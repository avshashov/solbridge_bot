from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import PreOrders


async def preorder_exists(session: AsyncSession, user_id, product):
    order = (await session.execute(select(PreOrders.order_id).where(PreOrders.user_id == user_id,
                                                                    PreOrders.product == product))).first()
    return True if order else False


async def create_preorder(session: AsyncSession, user_id, product, status):
    session.add(PreOrders(user_id=user_id, product=product, status=status))
    await session.commit()
