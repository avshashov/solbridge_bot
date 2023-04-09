import sqlalchemy.exc
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Users, Orders
from utils import get_hash


async def order_exists_db(session: AsyncSession, user_id, product) -> bool:
    order = (await session.execute(select(Orders.order_id).where(Orders.user_id == user_id, Orders.product == product,
                                                                 Orders.open == True,
                                                                 Orders.paid == False))).first()
    return True if order else False


async def create_order_db(session: AsyncSession, user_id, product, **kwargs) -> int:
    while True:
        try:
            hash_id = get_hash()
            session.add(Orders(order_id=hash_id, user_id=user_id, product=product, **kwargs))
            await session.commit()
            return hash_id
        except sqlalchemy.exc.IntegrityError:
            continue


async def cancel_order_by_user_db(session: AsyncSession, user_id, product) -> int:
    order_id = (
        await session.execute(update(Orders).where(
            Orders.user_id == user_id,
            Orders.product == product,
            Orders.open == True).values(open=False, canceled=True).returning(Orders.order_id))).fetchone()[0]
    await session.commit()

    return order_id


async def cancel_order_by_admin_db(session: AsyncSession, order_id) -> int:
    user_id = (await session.execute(update(Orders).where(
        Orders.order_id == order_id).values(open=False, canceled=True).returning(Orders.user_id))).fetchone()[0]
    await session.commit()

    return user_id


async def order_message_for_admin_db(session: AsyncSession, order_id, product) -> str:
    users_order = (await session.execute(select(Orders.url, Orders.created_at, Users.name).join(Users).where(
        Orders.order_id == order_id))).first()

    text = f'\n<b>Order</b>: {order_id}' \
           f'\n<b>Product</b>: {product}' \
           f'\n<b>Name</b>: {users_order.name}' \
           f'\n<b>URL</b>: {users_order.url}' \
           f'\n<b>Created at</b>: {users_order.created_at.strftime("%H:%M %d.%m.%Y")}'
    return text


async def get_orders_db(session: AsyncSession, product, open, paid, canceled) -> list:
    orders = (await session.execute(select(Orders.order_id).where(Orders.product == product,
                                                                  Orders.open == open, Orders.paid == paid,
                                                                  Orders.canceled == canceled))).all()
    return orders


async def get_order_more_db(session: AsyncSession, order_id) -> str:
    order = (await session.execute(select(Orders.order_id, Users.name, Users.username, Users.email, Users.instagram,
                                          Orders.created_at, Orders.url).join(Users).where(Orders.order_id ==
                                                                                           order_id))).first()

    text = text_order(order)
    return text


async def get_closed_orders_db(session: AsyncSession, product, canceled, paid=None) -> list:
    if paid:
        query = select(Orders.order_id, Users.name, Users.username, Users.email, Users.instagram,
                       Orders.created_at, Orders.url).join(Users).where(Orders.product == product,
                                                                        Orders.open == False,
                                                                        Orders.paid == paid,
                                                                        Orders.canceled == canceled)
    else:
        query = select(Orders.order_id, Users.name, Users.username, Users.email, Users.instagram,
                       Orders.created_at, Orders.url).join(Users).where(Orders.product == product,
                                                                        Orders.open == False,
                                                                        Orders.canceled == canceled)
    orders = (await session.execute(query)).all()

    result = []
    if orders:
        for order in orders:
            text = text_order(order)
            result.append(text)
    return result


async def approve_the_order_db(session: AsyncSession, order_id) -> int:
    user_id = (await session.execute(update(Orders).where(Orders.order_id == order_id).values(paid=True).returning(
        Orders.user_id))).fetchone()[0]

    await session.commit()
    return user_id


async def complete_the_order_db(session: AsyncSession, order_id) -> None:
    await session.execute(update(Orders).where(Orders.order_id == order_id).values(open=False))
    await session.commit()


async def get_order_user_db(session: AsyncSession, order_id) -> int:
    user_id = (await session.execute(select(Orders.user_id).where(Orders.order_id == order_id))).first()
    return user_id[0]


def text_order(order):
    text = f'<b>Order number</b>: {order.order_id}' \
           f'\n<b>Name</b>: {order.name}' \
           f'\n<b>Username</b>: {order.username}' \
           f'\n<b>Email</b>: {order.email}' \
           f'\n<b>Instagram</b>: {order.instagram}' \
           f'\n<b>URL</b>: {order.url}' \
           f'\n<b>Created at</b>: {order.created_at.strftime("%H:%M %d.%m.%Y")}'
    return text
