from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Users


async def get_user_info_db(session: AsyncSession, user_id: int) -> Users | None:
    user = (
        await session.execute(select(Users.name, Users.email, Users.instagram).where(Users.user_id == user_id))).first()
    return user


async def user_exists_db(session: AsyncSession, user_id: int) -> bool:
    user = (await session.execute(select(Users).where(Users.user_id == user_id))).first()
    return True if user else False


async def update_user_db(session: AsyncSession, user_id: int, name: str = None, email: str = None,
                         instagram: str = None) -> None:
    if name:
        await session.execute(update(Users).where(Users.user_id == user_id).values(name=name))
    if email:
        await session.execute(update(Users).where(Users.user_id == user_id).values(email=email))
    if instagram:
        await session.execute(update(Users).where(Users.user_id == user_id).values(instagram=instagram))

    await session.commit()


async def create_user_db(session: AsyncSession, user_id: int, name: str, username: str, email: str,
                         instagram: str) -> None:
    session.add(Users(user_id=user_id, name=name, username=username, email=email, instagram=instagram))
    await session.commit()
