from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import PreOrders


async def order_exists(session: AsyncSession, user_id, product):
    order = (await session.execute(select(PreOrders.order_id).where(PreOrders.user_id == user_id,
                                                                    PreOrders.product == product))).first()
    return True if order else False


async def create_order(session: AsyncSession, user_id, product, status):
    session.add(PreOrders(user_id=user_id, product=product, status=status))
    await session.commit()


async def statistics(session: AsyncSession):
    result = (await session.execute(
        select(PreOrders.product, PreOrders.status, func.count()).group_by(PreOrders.product,
                                                                           PreOrders.status).order_by(
            PreOrders.product, PreOrders.status))).all()

    if result:
        result = [' '.join(list(map(str, row))) for row in result]
        text = '\n'.join(result)
    else:
        text = 'The list is empty'
    return text
