import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
import os
from dotenv import load_dotenv

from handlers import user_handlers, admin

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
sol_bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')


async def set_commands(bot):
    commands = [
        BotCommand(command="/start", description="Start"),
        BotCommand(command="/help", description="Help")
    ]
    await bot.set_my_commands(commands)


async def main(bot):
    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    dp.include_router(admin.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main(sol_bot))
