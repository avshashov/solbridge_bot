import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import BotCommand

from bot import SingleBot
from handlers.photo_uploader import router as uploader_router
from handlers.admin import router as admin_router
from handlers.orders import router as orders_router
from solbot_db.db_orm import BotDB
from solbot_db.models import create_tables

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

sol_bot = SingleBot()


async def set_commands(bot):
    commands = [
        BotCommand(command='/start', description='Start'),
        BotCommand(command='/help', description='Help')
    ]
    await bot.set_my_commands(commands)


async def main(bot):
    create_tables(BotDB().engine)
    dp = Dispatcher()
    dp.include_router(uploader_router)
    dp.include_router(admin_router)
    dp.include_router(orders_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main(sol_bot))
