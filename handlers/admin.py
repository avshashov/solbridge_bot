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


@router.callback_query(F.data.split()[0] == 'Publish')
async def publish_post(callback: types.CallbackQuery):
    text = callback.message.html_text

    if callback.message.photo:
        await sol_bot.send_photo(chat_id=os.getenv('MAIN_GROUP_ID'), message_thread_id=os.getenv('TOPIC_ID'),
                                 photo=callback.message.photo[-1].file_id, caption=text)
    elif callback.message.document:
        await sol_bot.send_document(chat_id=os.getenv('MAIN_GROUP_ID'), message_thread_id=os.getenv('TOPIC_ID'),
                                    document=callback.message.document.file_id, caption=text)

    await callback.message.delete_reply_markup()
    await callback.message.edit_caption(caption=f'{text}\n\n<b>[Published]</b>')

    user_id = callback.data.split()[1]
    # try/except
    await sol_bot.send_message(chat_id=user_id, text='Your Photo was approved by Admin!')
    await callback.answer()


@router.callback_query(F.data.split()[0] == 'Collection')
async def publish_to_collection(callback: types.CallbackQuery):
    text = callback.message.html_text

    if callback.message.photo:
        await sol_bot.send_photo(chat_id=os.getenv('MAIN_GROUP_ID'), message_thread_id=os.getenv('TOPIC_ID'),
                                 photo=callback.message.photo[-1].file_id, caption=text)
        await sol_bot.send_photo(chat_id=os.getenv('CHANNEL_ID'), photo=callback.message.photo[-1].file_id,
                                 caption=text)
    elif callback.message.document:
        await sol_bot.send_document(chat_id=os.getenv('MAIN_GROUP_ID'), message_thread_id=os.getenv('TOPIC_ID'),
                                    document=callback.message.document.file_id, caption=text)
        await sol_bot.send_document(chat_id=os.getenv('CHANNEL_ID'), document=callback.message.document.file_id,
                                    caption=text)

    await callback.message.delete_reply_markup()
    await callback.message.edit_caption(caption=f'{text}\n\n<b>[Published to Collection]</b>')

    user_id = callback.data.split()[1]
    # try/except
    await sol_bot.send_message(chat_id=user_id, text='Congratulations! Your photo was included in the club\'s '
                                                     'collection!')
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
