import os

from aiogram import F, Router, types
from aiogram.filters import Command
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from bot import SingleBot
from database.pre_orders import statistics

load_dotenv()
sol_bot = SingleBot()
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
    await callback.message.edit_caption(caption=f'{text}\n\n<b>[Published]</b>')
    await callback.answer()


@router.callback_query(F.data == 'Reject')
async def reject_post(callback: types.CallbackQuery):
    text = callback.message.caption
    await callback.message.delete_reply_markup()
    await callback.message.edit_caption(caption=f'{text}\n\n<b>[Rejected]</b>')
    await callback.answer()


@router.message(F.chat.type != 'private', Command(commands=['orders']))
async def get_orders_statistic(message: types.Message, session: AsyncSession):
    if message.chat.id == int(os.getenv('TEST_GROUP')):
        text = await statistics(session)
        await message.answer(text)
