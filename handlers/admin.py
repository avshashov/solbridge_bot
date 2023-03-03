import os

from aiogram import F, Bot, Router, types
from dotenv import load_dotenv

load_dotenv()

sol_bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')
router = Router()


@router.callback_query(F.data == 'Publish')
async def publish_post(callback: types.CallbackQuery):
    text = callback.message.caption

    if callback.message.photo:
        await sol_bot.send_photo(chat_id=os.getenv('CHANNEL_ID'), photo=callback.message.photo[-1].file_id,
                                 caption=text)
    elif callback.message.document:
        await sol_bot.send_document(chat_id=os.getenv('CHANNEL_ID'), document=callback.message.document.file_id,
                                    caption=text)
    await callback.message.delete_reply_markup()
    await callback.message.reply(text='Published')
    await callback.answer()


@router.callback_query(F.data == 'Reject')
async def reject_post(callback: types.CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.message.reply(text='Rejected')
    await callback.answer()
