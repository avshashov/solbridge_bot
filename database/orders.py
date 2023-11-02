import sqlalchemy.exc
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Users, Orders
from utils import get_hash


async def order_exists_db(session: AsyncSession, user_id: int, product: str) -> int | None:
    stmt = (
        select(Orders.order_id).
        where(Orders.user_id == user_id,
              Orders.product == product,
              Orders.open.is_(True),
              Orders.paid.is_(False))
    )
    order = await session.execute(stmt)
    return order.first()


async def create_order_db(session: AsyncSession, user_id: int, product: str, **kwargs) -> str:
    while True:
        try:
            hash_id = get_hash()
            session.add(Orders(order_id=hash_id, user_id=user_id, product=product, **kwargs))
            await session.commit()
            return hash_id
        except sqlalchemy.exc.IntegrityError:
            continue


async def cancel_order_by_user_db(session: AsyncSession, user_id: int, product: str) -> int:
    stmt = (
        update(Orders).
        where(Orders.user_id == user_id,
              Orders.product == product,
              Orders.open.is_(True)).
        values(open=False, canceled=True).
        returning(Orders.order_id)
    )
    order_id = await session.execute(stmt)
    await session.commit()

    return order_id.fetchone()[0]


async def cancel_order_by_admin_db(session: AsyncSession, order_id: str) -> int:
    stmt = (
        update(Orders).
        where(Orders.order_id == order_id).
        values(open=False, canceled=True).
        returning(Orders.user_id)
    )
    user_id = await session.execute(stmt)
    await session.commit()

    return user_id.fetchone()[0]


async def order_message_for_admin_db(session: AsyncSession, order_id: str, product: str) -> str:
    stmt = (
        select(Orders.url, Orders.created_at, Users.name).
        join(Users).
        where(Orders.order_id == order_id)
    )
    users_order = (await session.execute(stmt)).first()

    text = f'\n<b>Order</b>: {order_id}' \
           f'\n<b>Product</b>: {product}' \
           f'\n<b>Name</b>: {users_order.name}' \
           f'\n<b>URL</b>: {users_order.url}' \
           f'\n<b>Created at</b>: {users_order.created_at.strftime("%H:%M %d.%m.%Y")}'
    return text


async def get_orders_db(session: AsyncSession, product: str, open: bool, paid: bool, canceled: bool) -> list:
    stmt = (
        select(Orders.order_id).
        where(Orders.product == product,
              Orders.open == open,
              Orders.paid == paid,
              Orders.canceled == canceled)
    )
    orders = (await session.execute(stmt)).all()
    return list(orders)


async def get_order_more_db(session: AsyncSession, order_id: str) -> str:
    stmt = (
        select(Orders.order_id,
               Users.name,
               Users.username,
               Users.email,
               Users.instagram,
               Orders.created_at,
               Orders.url).
        join(Users).
        where(Orders.order_id == order_id)
    )
    order = (await session.execute(stmt)).first()

    text = text_order(order)
    return text


async def get_closed_orders_db(session: AsyncSession, product: str, canceled: bool, paid: bool | None = None) -> list:
    params = {
        Orders.product == product,
        Orders.open.is_(False),
        Orders.canceled == canceled
    }
    if paid:
        params.add(Orders.paid == paid)

    stmt = (
        select(Orders.order_id,
               Users.name,
               Users.username,
               Users.email,
               Users.instagram,
               Orders.created_at,
               Orders.url).
        join(Users).
        where(*params)
    )
    orders = (await session.execute(stmt)).all()

    result = [text_order(order) for order in orders]
    return result


async def approve_the_order_db(session: AsyncSession, order_id: str) -> int:
    stmt = (
        update(Orders).
        where(Orders.order_id == order_id).
        values(paid=True).
        returning(Orders.user_id)
    )
    user_id = (await session.execute(stmt)).fetchone()[0]

    await session.commit()
    return user_id


async def complete_the_order_db(session: AsyncSession, order_id: str) -> None:
    stmt = (
        update(Orders).
        where(Orders.order_id == order_id).
        values(open=False)
    )
    await session.execute(stmt)
    await session.commit()


async def get_order_user_db(session: AsyncSession, order_id: str) -> int:
    stmt = select(Orders.user_id).where(Orders.order_id == order_id)
    user_id = (await session.execute(stmt)).first()
    return user_id[0]


def get_stmt_for_select_query(product: str, paid: bool) -> select:
    stmt = (
        select(Users.email).
        join(Orders).
        where(Orders.product == product,
              Orders.open.is_(True),
              Orders.paid.is_(paid))
    )

    return stmt


async def get_emails_db(session: AsyncSession) -> str:
    paid_albums = (await session.execute(get_stmt_for_select_query(product='album', paid=True))).scalars().all()
    paid_albums = '\n'.join(paid_albums) if paid_albums else 'The list is empty'

    unpaid_albums = (await session.execute(get_stmt_for_select_query(product='album', paid=False))).scalars().all()
    unpaid_albums = '\n'.join(unpaid_albums) if unpaid_albums else 'The list is empty'

    paid_books = (await session.execute(get_stmt_for_select_query(product='book', paid=True))).scalars().all()
    paid_books = '\n'.join(paid_books) if paid_books else 'The list is empty'

    unpaid_books = (await session.execute(get_stmt_for_select_query(product='book', paid=False))).scalars().all()
    unpaid_books = '\n'.join(unpaid_books) if unpaid_books else 'The list is empty'

    text = f'<b>Email list</b>' \
           f'\n\nPaid albums:' \
           f'\n{paid_albums}' \
           f'\n\nUnpaid albums:' \
           f'\n{unpaid_albums}' \
           f'\n\nPaid books:' \
           f'\n{paid_books}' \
           f'\n\nUnpaid books:' \
           f'\n{unpaid_books}'

    return text


def text_order(order) -> str:
    text = f'<b>Order number</b>: {order.order_id}' \
           f'\n<b>Name</b>: {order.name}' \
           f'\n<b>Username</b>: {order.username}' \
           f'\n<b>Email</b>: {order.email}' \
           f'\n<b>Instagram</b>: {order.instagram}' \
           f'\n<b>URL</b>: {order.url}' \
           f'\n<b>Created at</b>: {order.created_at.strftime("%H:%M %d.%m.%Y")}'
    return text
