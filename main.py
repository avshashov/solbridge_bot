import asyncio
import logging
import os

from aiogram import Dispatcher
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot import SingleBot
from database.models import Base
import job
from handlers.photo_uploader import router as uploader_router
from handlers.admin import router as admin_router
from handlers.orders import router as orders_router
from middlewares.session_db import SessionMiddleware

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

sol_bot = SingleBot()


async def set_commands(bot):
    commands = [
        BotCommand(command='/start', description='Start'),
        BotCommand(command='/help', description='Help')
    ]
    await bot.set_my_commands(commands)


async def main(bot):
    DSN = f'postgresql+asyncpg://{os.getenv("USER_DB")}:{os.getenv("PASSWORD_DB")}@{os.getenv("HOST_DB")}:5432' \
          f'/{os.getenv("NAME_DB")}'
    engine = create_async_engine(DSN, echo=False, future=True)
    session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    dp = Dispatcher()
    dp.update.middleware.register(SessionMiddleware(session))
    dp.include_router(uploader_router)
    dp.include_router(admin_router)
    dp.include_router(orders_router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(job.send_post, trigger='cron',
                      hour='10-21', minute='*/20', timezone='Asia/Seoul',
                      args=(session,))
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main(sol_bot))
