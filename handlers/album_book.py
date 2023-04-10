import os

from aiogram import Router, types, F
from aiogram.filters import Text
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from bot import SingleBot
from database.pre_orders import order_exists, create_order
from keybords.callback_buttons import pre_order_choice_kb

load_dotenv()
sol_bot = SingleBot()
router = Router()


@router.message(Text(text=['Photo Album']))
async def press_photo_album(message: types.Message, session: AsyncSession):
    text = 'We will begin offering the photo album with 30 of your photos' \
           ' to preserve your memories starting on May 15th. ' \
           'Priced at 18,000₩ for one album with 30 photos.' \
           '\n\nFollow our instagram and be ready for updates 😎'

    if await order_exists(session, user_id=message.from_user.id, product='album'):
        await message.answer(text)
    else:
        await message.answer(text, reply_markup=pre_order_choice_kb(product='album'))


@router.message(Text(text=['PCS Book']))
async def press_pcs_book(message: types.Message, session: AsyncSession):
    text = 'Some text (book)'
    if await order_exists(session, user_id=message.from_user.id, product='book'):
        await message.answer(text)
    else:
        await message.answer(text, reply_markup=pre_order_choice_kb(product='book'))


@router.callback_query(F.data.split()[0].in_({'buy', 'think', 'no'}))
async def set_order_status(callback: types.CallbackQuery, session: AsyncSession):
    status, product = callback.data.split()
    user_id = callback.from_user.id

    await create_order(session, user_id=user_id, product=product, status=status)
    await sol_bot.send_message(chat_id=os.getenv('TEST_GROUP'), text=f'{product}, {user_id}, {status}')

    await callback.message.edit_text(text='Thanks for the answer')
    await callback.answer()
