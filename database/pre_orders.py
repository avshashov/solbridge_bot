from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import PreOrders


async def preorder_exists(session: AsyncSession, user_id: int, product: str) -> bool:
    stmt = (
        select(PreOrders.order_id).
        where(PreOrders.user_id == user_id, PreOrders.product == product)
    )
    order = (await session.execute(stmt)).first()
    return bool(order)


async def create_preorder(session: AsyncSession, user_id: int, product: str, status: str) -> None:
    session.add(PreOrders(user_id=user_id, product=product, status=status))
    await session.commit()
