import os
from random import choice

from aiogram.exceptions import TelegramForbiddenError
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot import SingleBot
from database.queue import get_post_from_queue, change_post_status
import phrases

sol_bot = SingleBot()


async def send_post(sessionmaker: async_sessionmaker) -> None:
    post = await get_post_from_queue(sessionmaker)

    if not post:
        return

    if post.type == 'photo':
        await sol_bot.send_photo(chat_id=os.getenv('TOPIC_GROUP_ID'),
                                 message_thread_id=os.getenv('TOPIC_THREAD_ID'),
                                 photo=post.file_id,
                                 caption=post.text)
        if post.target:
            await sol_bot.send_photo(chat_id=os.getenv('COLLECTION_CHANNEL_ID'),
                                     photo=post.file_id,
                                     caption=post.text)
    elif post.type == 'document':
        await sol_bot.send_document(chat_id=os.getenv('TOPIC_GROUP_ID'),
                                    message_thread_id=os.getenv('TOPIC_THREAD_ID'),
                                    document=post.file_id,
                                    caption=post.text)
        if post.target:
            await sol_bot.send_document(chat_id=os.getenv('COLLECTION_CHANNEL_ID'),
                                        document=post.file_id,
                                        caption=post.text)

    try:
        if post.target:
            await sol_bot.send_message(chat_id=post.user_id,
                                       text=choice(phrases.user_notification_phrases['Collection']))
        else:
            await sol_bot.send_message(chat_id=post.user_id,
                                       text=choice(phrases.user_notification_phrases['Approve']))
    except TelegramForbiddenError:
        pass

    await change_post_status(sessionmaker, id=post.id)
