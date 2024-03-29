import os

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession

import phrases
from bot import SingleBot
from database import orders as db, queue
from keybords import callback_buttons

sol_bot = SingleBot()
router = Router()


@router.callback_query(F.data.split()[0] == 'Publish')
async def publish_post(callback: types.CallbackQuery, session: AsyncSession):
    text = callback.message.html_text
    user_id = int(callback.data.split()[1])

    if callback.message.photo:
        photo_id = callback.message.photo[-1].file_id
        await queue.add_post_to_queue(session, user_id=user_id, type='photo', text=text, file_id=photo_id, target=False)

    elif callback.message.document:
        document_id = callback.message.document.file_id
        await queue.add_post_to_queue(session, user_id=user_id, type='document', text=text, file_id=document_id,
                                      target=False)

    await callback.message.delete_reply_markup()
    await callback.message.edit_caption(caption=f'{text}\n\n<b>[Approved]</b>')

    await callback.answer()


@router.callback_query(F.data.split()[0] == 'Collection')
async def publish_to_collection(callback: types.CallbackQuery, session: AsyncSession):
    text = callback.message.html_text
    user_id = int(callback.data.split()[1])

    if callback.message.photo:
        photo_id = callback.message.photo[-1].file_id
        await queue.add_post_to_queue(session, user_id=user_id, type='photo', text=text, file_id=photo_id, target=True)

    elif callback.message.document:
        document_id = callback.message.document.file_id
        await queue.add_post_to_queue(session, user_id=user_id, type='document', text=text, file_id=document_id,
                                      target=True)

    await callback.message.delete_reply_markup()
    await callback.message.edit_caption(caption=f'{text}\n\n<b>[Published to Collection]</b>')

    await callback.answer()


@router.callback_query(F.data == 'Reject')
async def reject_post(callback: types.CallbackQuery):
    text = callback.message.html_text
    await callback.message.delete_reply_markup()
    await callback.message.edit_caption(caption=f'{text}\n\n<b>[Rejected]</b>')
    await callback.answer()


@router.message(F.chat.type != 'private', Command(commands=['orders']))
async def orders_command(message: types.Message):
    if message.chat.id == int(os.getenv('ADMIN_ORDERS')):
        await message.answer(text='Select order category', reply_markup=callback_buttons.orders_category_kb())


@router.message(F.chat.type != 'private', Command(commands=['emails']))
async def emails_command(message: types.Message, session: AsyncSession):
    if message.chat.id == int(os.getenv('ADMIN_ORDERS')):
        emails = await db.get_emails_db(session)
        await message.answer(text=emails)


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


@router.callback_query(F.data.in_(
    {
        'paid album',
        'unpaid album',
        'paid book',
        'unpaid book',
        'Back to orders',
        'previous page',
        'next page'
    }
))
async def get_paid_unpaid_orders(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback.data == 'Back to orders':
        data = await state.get_data()
        status, product, offset = data['status'], data['product'], data['offset']

    elif callback.data == 'previous page':
        data = await state.get_data()
        status, product, offset = data['status'], data['product'], data['offset'] - 5
        await state.update_data(offset=offset)

    elif callback.data == 'next page':
        data = await state.get_data()
        status, product, offset = data['status'], data['product'], data['offset'] + 5
        await state.update_data(offset=offset)

    else:
        offset = 0
        status, product = callback.data.split()
        await state.update_data(product=product, status=status, offset=offset)

    paid = True if status == 'paid' else False
    orders = await db.get_orders_db(session, product=product, open=True, canceled=False, paid=paid)
    count = len(orders)
    await callback.message.edit_text(text=f'{status.title()} orders list ({product})',
                                     reply_markup=callback_buttons.orders_kb(product=product, orders=orders,
                                                                             count=count, offset=offset))
    await callback.answer()


@router.callback_query(F.data.in_({'back paid/unpaid album', 'back paid/unpaid book'}))
async def back_paid_unpaid_orders(callback: types.CallbackQuery):
    product = callback.data.split()[-1]
    await callback.message.edit_text(text=f'{product.title()}.\n\nSelect paid/unpaid orders:',
                                     reply_markup=callback_buttons.paid_unpaid_orders_kb(product=product))
    await callback.answer()


@router.callback_query(F.data.split()[0] == 'order')
async def order_more(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    order_id = callback.data.split()[1]
    text = await db.get_order_more_db(session, order_id=order_id)
    data = await state.get_data()
    if data['status'] == 'paid':
        await callback.message.edit_text(text=text, reply_markup=callback_buttons.paid_order_more_kb(order_id))
    elif data['status'] == 'unpaid':
        await callback.message.edit_text(text=text, reply_markup=callback_buttons.unpaid_order_more_kb(order_id))

    await callback.answer()


@router.callback_query(F.data.in_({'completed album', 'completed book', 'canceled album', 'canceled book'}))
async def get_completed_canceled_orders(callback: types.CallbackQuery, session: AsyncSession):
    status, product = callback.data.split()
    orders = []
    if status == 'completed':
        orders = await db.get_closed_orders_db(session, product=product, canceled=False, paid=True)
    elif status == 'canceled':
        orders = await db.get_closed_orders_db(session, product=product, canceled=True)
    orders = '\n\n'.join(orders) if orders else 'The list is empty'
    try:
        await callback.message.edit_text(text=f'{status.title()} {product}:\n\n{orders}',
                                         reply_markup=callback_buttons.closed_orders_kb(product))
    except TelegramBadRequest:
        pass
    await callback.answer()


@router.callback_query(F.data.split()[0] == 'Cancel')
async def cancel_order(callback: types.CallbackQuery, session: AsyncSession):
    order_id = callback.data.split()[1]
    user_id = await db.cancel_order_by_admin_db(session, order_id)
    await callback.message.edit_text(text=f'Order {order_id} canceled',
                                     reply_markup=callback_buttons.back_orders())

    await sol_bot.send_message(chat_id=user_id, text=f'{phrases.order_phrases["cancel_the_order"]}'
                                                     f'\nOrder {order_id}')
    await callback.answer()


@router.callback_query(F.data.split()[0] == 'Approve')
async def approve_order(callback: types.CallbackQuery, session: AsyncSession):
    order_id = callback.data.split()[1]
    user_id = await db.approve_the_order_db(session, order_id)
    await callback.message.edit_text(text=f'Order {order_id} approved',
                                     reply_markup=callback_buttons.back_orders())

    await sol_bot.send_message(chat_id=user_id, text=f'{phrases.order_phrases["approve_the_order"]}'
                                                     f'\nOrder {order_id}')
    await callback.answer()


@router.callback_query(F.data.split()[0] == 'Complete')
async def complete_order(callback: types.CallbackQuery, session: AsyncSession):
    order_id = callback.data.split()[1]
    await db.complete_the_order_db(session, order_id)
    await callback.message.edit_text(text=f'Order {order_id} completed',
                                     reply_markup=callback_buttons.back_orders())

    await callback.answer()


@router.callback_query(F.data.split()[0] == 'Notify')
async def notify_order(callback: types.CallbackQuery, session: AsyncSession):
    order_id = callback.data.split()[1]
    user_id = await db.get_order_user_db(session, order_id)
    await callback.message.edit_text(text=f'the user is notified that the order {order_id} is ready',
                                     reply_markup=callback_buttons.back_orders())

    await sol_bot.send_message(chat_id=user_id, text=f'Order {order_id} is ready.')
    await callback.answer()
