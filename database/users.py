from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Users


async def get_user_info_db(session: AsyncSession, user_id: int) -> Users | None:
    stmt = (
        select(Users.name, Users.email, Users.instagram).
        where(Users.user_id == user_id)
    )
    user = (await session.execute(stmt)).first()
    return user


async def user_exists_db(session: AsyncSession, user_id: int) -> bool:
    stmt = select(Users).where(Users.user_id == user_id)
    user = (await session.execute(stmt)).first()
    return bool(user)


async def update_user_db(session: AsyncSession,
                         user_id: int,
                         name: str = None,
                         email: str = None,
                         instagram: str = None) -> None:
    params = {}
    if name:
        params.update({'name': name})
    if email:
        params.update({'email': email})
    if instagram:
        params.update({'instagram': instagram})

    stmt = update(Users).where(Users.user_id == user_id).values(**params)
    await session.execute(stmt)

    await session.commit()


async def create_user_db(session: AsyncSession,
                         user_id: int,
                         name: str,
                         username: str,
                         email: str,
                         instagram: str) -> None:
    session.add(Users(user_id=user_id, name=name, username=username, email=email, instagram=instagram))
    await session.commit()
