import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import BotCommand

from bot import SingleBot
from handlers.user_handlers import router as uh_router
from handlers.admin import router as admin_router

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

sol_bot = SingleBot()


async def set_commands(bot):
    commands = [
        BotCommand(command='/start', description='Start'),
        BotCommand(command='/help', description='Help')
    ]
    await bot.set_my_commands(commands)


async def main(bot):
    dp = Dispatcher()
    dp.include_router(uh_router)
    dp.include_router(admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main(sol_bot))
