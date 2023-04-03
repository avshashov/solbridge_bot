import os

from aiogram import F, Router, types
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv

from bot import SingleBot
from keybords import callback_buttons
from solbot_db.db_orm import BotDB


class OrderData(StatesGroup):
    pass


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
    await callback.message.reply(text='Published')
    await callback.answer()


@router.callback_query(F.data == 'Reject')
async def reject_post(callback: types.CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.message.reply(text='Rejected')
    await callback.answer()


@router.message(Command(commands=['orders']))
async def orders_command(message: types.Message):
    if message.chat.id == int(os.getenv('GROUP_ID')):
        await message.answer(text='Select order category', reply_markup=callback_buttons.orders_category_kb())


@router.callback_query(F.data.in_({'admin album', 'admin book'}))
async def select_order_category(callback: types.CallbackQuery):
    product = callback.data.split()[-1]
    await callback.message.edit_text(text=f'{product.title()}.\n\nSelect order type:',
                                     reply_markup=callback_buttons.open_closed_orders_kb(product=product))
    await callback.answer()


@router.callback_query(F.data.in_({'open album', 'closed album', 'open book', 'closed book'}))
async def select_open_closed_orders(callback: types.CallbackQuery):
    status, product = callback.data.split()
    if status == 'open':
        await callback.message.edit_text(text=f'{product.title()}.\n\nSelect paid/unpaid orders:',
                                         reply_markup=callback_buttons.paid_unpaid_orders_kb(product=product))
    elif status == 'closed':
        await callback.message.edit_text(text=f'{product.title()}.\n\nSelect completed/canceled orders:',
                                         reply_markup=callback_buttons.closed_orders_kb(product=product))

    await callback.answer()


@router.callback_query(F.data.in_({'back album', 'back book'}))
async def back_type_orders(callback: types.CallbackQuery):
    await callback.message.edit_text(text='Select order category',
                                     reply_markup=callback_buttons.orders_category_kb())
    await callback.answer()


@router.callback_query(F.data.in_({'back open/closed album', 'back open/closed book'}))
async def back_open_closed_orders(callback: types.CallbackQuery):
    product = callback.data.split()[-1]
    await callback.message.edit_text(text=f'{product.title()}.\n\nSelect order type:',
                                     reply_markup=callback_buttons.open_closed_orders_kb(product=product))
    await callback.answer()


@router.callback_query(F.data.in_({'paid album', 'unpaid album', 'paid book', 'unpaid book'}))
async def get_paid_unpaid_orders(callback: types.CallbackQuery, state: FSMContext):
    status, product = callback.data.split()
    if status == 'paid':
        await callback.message.edit_text(text=f'Paid orders list ({product})',
                                         reply_markup=callback_buttons.orders_kb(product=product, open=True,
                                                                                 canceled=False, paid=True))
    elif status == 'unpaid':
        await callback.message.edit_text(text=f'Unpaid orders list ({product})',
                                         reply_markup=callback_buttons.orders_kb(product=product, open=True,
                                                                                 canceled=False, paid=False))

    await state.update_data(product=product, status=status)
    await callback.answer()


@router.callback_query(F.data.in_({'back paid/unpaid album', 'back paid/unpaid book'}))
async def back_paid_unpaid_orders(callback: types.CallbackQuery):
    product = callback.data.split()[-1]
    await callback.message.edit_text(text=f'{product.title()}.\n\nSelect paid/unpaid orders:',
                                     reply_markup=callback_buttons.paid_unpaid_orders_kb(product=product))
    await callback.answer()


@router.callback_query(F.data.split()[0] == 'order')
async def order_more(callback: types.CallbackQuery, state: FSMContext):
    text = BotDB().get_order_more(order_id=callback.data.split()[1])
    data = await state.get_data()
    if data['status'] == 'paid':
        await callback.message.edit_text(text=text, reply_markup=callback_buttons.paid_order_more_kb())
    elif data['status'] == 'unpaid':
        await callback.message.edit_text(text=text, reply_markup=callback_buttons.unpaid_order_more_kb())

    await callback.answer()


@router.callback_query(F.data == 'Back to orders')
async def back_to_orders(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    status, product = data['status'], data['product']
    if status == 'paid':
        await callback.message.edit_text(text=f'Paid orders list ({product})',
                                         reply_markup=callback_buttons.orders_kb(product=product, open=True,
                                                                                 canceled=False, paid=True))
    elif status == 'unpaid':
        await callback.message.edit_text(text=f'Unpaid orders list ({product})',
                                         reply_markup=callback_buttons.orders_kb(product=product, open=True,
                                                                                 canceled=False, paid=False))

    await callback.answer()


@router.callback_query(F.data.in_({'completed album', 'completed book', 'canceled album', 'canceled book'}))
async def get_completed_canceled_orders(callback: types.CallbackQuery):
    status, product = callback.data.split()
    orders = []
    if status == 'completed':
        orders = BotDB().get_orders_more(product=product, open=False, paid=True, canceled=False)
    elif status == 'canceled':
        paid_orders = BotDB().get_orders_more(product=product, open=False, paid=True, canceled=True)
        unpaid_orders = BotDB().get_orders_more(product=product, open=False, paid=False, canceled=True)
        orders = paid_orders + unpaid_orders

    orders = '\n\n'.join(orders) if orders else 'The list is empty'
    await callback.message.edit_text(text=f'{status.title()} {product}:\n\n{orders}',
                                     reply_markup=callback_buttons.closed_orders_kb(product))
    await callback.answer()
