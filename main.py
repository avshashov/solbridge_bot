import asyncio

from aiogram import Dispatcher, Bot
from settings import bot_token

mybot = Bot(token=bot_token)


async def main(bot):
    dp = Dispatcher()

    # dp.include_router()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main(mybot))
