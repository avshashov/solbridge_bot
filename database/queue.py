from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import PostQueue


async def add_post_to_queue(session: AsyncSession, user_id, type, text, file_id, target) -> None:
    session.add(PostQueue(status=False, user_id=user_id, type=type, text=text, file_id=file_id, target=target))
    await session.commit()


async def get_post_from_queue(sessionmaker) -> PostQueue | None:
    async with sessionmaker() as session:
        post = (await session.execute(select(PostQueue.id, PostQueue.user_id, PostQueue.type, PostQueue.text,
                                             PostQueue.file_id,
                                             PostQueue.target).where(PostQueue.status == False))).first()
        return post


async def change_post_status(sessionmaker, id) -> None:
    async with sessionmaker() as session:
        await session.execute(update(PostQueue).where(PostQueue.id == id).values(status=True))
        await session.commit()
