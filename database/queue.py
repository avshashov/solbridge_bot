from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.models import PostQueue


async def add_post_to_queue(session: AsyncSession,
                            user_id: int,
                            type: str,
                            text: str,
                            file_id: str,
                            target: bool) -> None:
    session.add(PostQueue(
        status=False,
        user_id=user_id,
        type=type,
        text=text,
        file_id=file_id,
        target=target
    ))
    await session.commit()


async def get_post_from_queue(sessionmaker: async_sessionmaker) -> PostQueue | None:
    stmt = (
        select(PostQueue.id,
               PostQueue.user_id,
               PostQueue.type,
               PostQueue.text,
               PostQueue.file_id,
               PostQueue.target).
        where(PostQueue.status.is_(False))
    )
    async with sessionmaker() as session:
        post = (await session.execute(stmt)).first()
        return post


async def change_post_status(sessionmaker: async_sessionmaker, id: int) -> None:
    stmt = update(PostQueue).where(PostQueue.id == id).values(status=True)
    async with sessionmaker() as session:
        await session.execute(stmt)
        await session.commit()
