import os
from random import choice

from aiogram import F, Router, types
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

import phrases
from bot import SingleBot
from database.pre_orders import statistics

load_dotenv()
sol_bot = SingleBot()
router = Router()


@router.callback_query(F.data.split()[0] == 'Publish')
async def publish_post(callback: types.CallbackQuery):
    text = callback.message.html_text

    if callback.message.photo:
        await sol_bot.send_photo(chat_id=os.getenv('TOPIC_GROUP_ID'), message_thread_id=os.getenv('TOPIC_THREAD_ID'),
                                 photo=callback.message.photo[-1].file_id, caption=text)
    elif callback.message.document:
        await sol_bot.send_document(chat_id=os.getenv('TOPIC_GROUP_ID'), message_thread_id=os.getenv('TOPIC_THREAD_ID'),
                                    document=callback.message.document.file_id, caption=text)

    await callback.message.delete_reply_markup()
    await callback.message.edit_caption(caption=f'{text}\n\n<b>[Approved]</b>')

    try:
        user_id = callback.data.split()[1]
        await sol_bot.send_message(chat_id=user_id, text=choice(phrases.user_notification_phrases['Approve']))
    except IndexError:
        pass
    except TelegramForbiddenError:
        pass
    await callback.answer()


@router.callback_query(F.data.split()[0] == 'Collection')
async def publish_to_collection(callback: types.CallbackQuery):
    text = callback.message.html_text

    if callback.message.photo:
        await sol_bot.send_photo(chat_id=os.getenv('TOPIC_GROUP_ID'), message_thread_id=os.getenv('TOPIC_THREAD_ID'),
                                 photo=callback.message.photo[-1].file_id, caption=text)
        await sol_bot.send_photo(chat_id=os.getenv('COLLECTION_CHANNEL_ID'), photo=callback.message.photo[-1].file_id,
                                 caption=text)
    elif callback.message.document:
        await sol_bot.send_document(chat_id=os.getenv('TOPIC_GROUP_ID'), message_thread_id=os.getenv('TOPIC_THREAD_ID'),
                                    document=callback.message.document.file_id, caption=text)
        await sol_bot.send_document(chat_id=os.getenv('COLLECTION_CHANNEL_ID'),
                                    document=callback.message.document.file_id,
                                    caption=text)

    await callback.message.delete_reply_markup()
    await callback.message.edit_caption(caption=f'{text}\n\n<b>[Published to Collection]</b>')

    user_id = callback.data.split()[1]
    try:
        await sol_bot.send_message(chat_id=user_id, text=choice(phrases.user_notification_phrases['Collection']))
    except TelegramForbiddenError:
        pass
    await callback.answer()


@router.callback_query(F.data == 'Reject')
async def reject_post(callback: types.CallbackQuery):
    text = callback.message.html_text
    await callback.message.delete_reply_markup()
    await callback.message.edit_caption(caption=f'{text}\n\n<b>[Rejected]</b>')
    await callback.answer()


@router.message(F.chat.type != 'private', Command(commands=['orders']))
async def get_orders_statistic(message: types.Message, session: AsyncSession):
    if message.chat.id == int(os.getenv('ADMIN_ORDERS')):
        text = await statistics(session)
        await message.answer(text)
