import asyncio
import logging

from aiogram import Dispatcher, Bot
from settings import bot_token
from handlers import user_handlers

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
sol_bot = Bot(token=bot_token, parse_mode='HTML')


async def main(bot):
    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main(sol_bot))
