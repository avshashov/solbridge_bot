import argparse
import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot import SingleBot
from config import SettingsDB, SettingsScheduler
from database.models import create_tables
import job
from handlers.photo_uploader import router as uploader_router
from handlers.admin import router as admin_router
from handlers.orders import router as orders_router
from middlewares.session_db import SessionMiddleware


def init_argparser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    return args


def init_dispatcher(sessionmaker: async_sessionmaker) -> Dispatcher:
    dp = Dispatcher()
    dp.update.middleware.register(SessionMiddleware(sessionmaker))
    dp.include_router(uploader_router)
    dp.include_router(admin_router)
    dp.include_router(orders_router)
    return dp


async def set_commands(bot):
    commands = [
        BotCommand(command='/start', description='Start'),
        BotCommand(command='/help', description='Help')
    ]
    await bot.set_my_commands(commands)


async def main():
    bot = SingleBot()
    args = init_argparser()
    debug_depth = logging.DEBUG if args.debug else logging.ERROR
    logging.basicConfig(level=debug_depth, format='%(asctime)s - %(levelname)s - %(message)s')

    settings_db = SettingsDB()
    engine = create_async_engine(settings_db.pg_dsn, echo=False, future=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    await create_tables(engine)

    dp = init_dispatcher(sessionmaker)

    scheduler = AsyncIOScheduler()
    settings_scheduler = SettingsScheduler()
    scheduler.add_job(job.send_post,
                      trigger=settings_scheduler.trigger,
                      hour=settings_scheduler.hour,
                      minute=settings_scheduler.minute,
                      timezone=settings_scheduler.timezone,
                      args=(sessionmaker,))
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
