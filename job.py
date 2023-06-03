import os
from random import choice

from aiogram.exceptions import TelegramForbiddenError
from dotenv import load_dotenv

from bot import SingleBot
from database.queue import get_post_from_queue, change_post_status
import phrases

load_dotenv()
sol_bot = SingleBot()


async def send_post(sessionmaker):
    post = await get_post_from_queue(sessionmaker)

    if post:
        id, user_id, type, = post.id, post.user_id, post.type,
        text, file_id, target = post.text, post.file_id, post.target

        if target:
            if type == 'photo':
                await sol_bot.send_photo(chat_id=os.getenv('TOPIC_GROUP_ID'),
                                         message_thread_id=os.getenv('TOPIC_THREAD_ID'),
                                         photo=file_id, caption=text)
                await sol_bot.send_photo(chat_id=os.getenv('COLLECTION_CHANNEL_ID'),
                                         photo=file_id,
                                         caption=text)
            if type == 'document':
                await sol_bot.send_document(chat_id=os.getenv('TOPIC_GROUP_ID'),
                                            message_thread_id=os.getenv('TOPIC_THREAD_ID'),
                                            document=file_id, caption=text)
                await sol_bot.send_document(chat_id=os.getenv('COLLECTION_CHANNEL_ID'),
                                            document=file_id,
                                            caption=text)
            try:
                await sol_bot.send_message(chat_id=user_id,
                                           text=choice(phrases.user_notification_phrases['Collection']))
            except TelegramForbiddenError:
                pass

        if not target:
            if type == 'photo':
                await sol_bot.send_photo(chat_id=os.getenv('TOPIC_GROUP_ID'),
                                         message_thread_id=os.getenv('TOPIC_THREAD_ID'),
                                         photo=file_id, caption=text)
            if type == 'document':
                await sol_bot.send_document(chat_id=os.getenv('TOPIC_GROUP_ID'),
                                            message_thread_id=os.getenv('TOPIC_THREAD_ID'),
                                            document=file_id, caption=text)

            try:
                await sol_bot.send_message(chat_id=user_id, text=choice(phrases.user_notification_phrases['Approve']))
            except TelegramForbiddenError:
                pass

        await change_post_status(sessionmaker, id=id)
