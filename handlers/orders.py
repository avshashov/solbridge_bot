import os

from aiogram import Router, types, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv

import phrases
from bot import SingleBot
from keybords import default_buttons, callback_buttons
from solbot_db.db_orm import BotDB


class UserData(StatesGroup):
    data_state = State()
    url_state = State()
    confirm_url_state = State()
    name_state = State()
    email_state = State()
    instagram_state = State()
    cancel_order_state = State()


load_dotenv()
sol_bot = SingleBot()
router = Router()


@router.message(F.text.in_({'Photo Album', 'PCS Book'}))
async def press_photoalbum_or_book(message: types.Message, state: FSMContext):
    if message.text == 'Photo Album':
        text = phrases.order_phrases['album']
        await message.answer(text=text, reply_markup=callback_buttons.order_photo_album_kb())
    elif message.text == 'PCS Book':
        text = phrases.order_phrases['book']
        await message.answer(text=text, reply_markup=callback_buttons.order_book_kb())


@router.callback_query(F.data.in_({'album', 'book'}))
async def order_photo_album(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(product=callback.data)

    if callback.data == 'album' and BotDB().order_exists(callback.from_user.id, product='album'):
        await callback.message.edit_text(text=phrases.order_phrases['exists_album'])
        await callback.message.answer(text='Choose an action', reply_markup=default_buttons.cancel_order_kb())
        await state.set_state(UserData.cancel_order_state)

    elif callback.data == 'book' and BotDB().order_exists(callback.from_user.id, product='book'):
        await callback.message.edit_text(text=phrases.order_phrases['exists_book'])
        await callback.message.answer(text='Choose an action', reply_markup=default_buttons.cancel_order_kb())
        await state.set_state(UserData.cancel_order_state)

    else:
        await callback.message.answer(text='Order formation stage', reply_markup=default_buttons.cancel_kb())

        if BotDB().user_exists(callback.from_user.id):
            user = BotDB().get_user_info(callback.from_user.id)
            await callback.message.answer(text=f'Please check all your information:'
                                               f'{text_user_info(user.name, user.email, user.instagram)}',
                                          reply_markup=callback_buttons.change_data_kb())

        else:
            await callback.message.answer(text='Could you tell me what is your name, please?')
            await state.set_state(UserData.name_state)
    await callback.answer()


@router.message(UserData.cancel_order_state, Text(text=['Undo Purchase']))
async def cancel_order(message: types.Message, state: FSMContext):
    product = await state.get_data()
    order_id = BotDB().cancel_order(user_id=message.from_user.id, product=product['product'])
    text = BotDB().order_message_for_admin(order_id=order_id, product=product['product'])

    await sol_bot.send_message(chat_id=os.getenv('GROUP_ID'), text=f'<b>[CANCELLED]</b>'
                                                                   f'\n{text}')
    await message.answer(text=f'Order №<b>{order_id}</b> is cancelled', reply_markup=default_buttons.main_menu_kb())
    await state.clear()


@router.message(UserData.name_state)
async def get_user_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserData.email_state)
    await message.reply(text='Roger that')
    await message.answer(text='What is your email? I need it to contact with you.')


@router.message(UserData.email_state)
async def get_user_name(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(UserData.instagram_state)
    await message.reply(text='Cool')
    await message.answer(text='I need also your instagram. '
                              'Just only as second option to send your important messages')


@router.message(UserData.instagram_state)
async def get_user_name(message: types.Message, state: FSMContext):
    await state.update_data(instagram=message.text)
    await message.reply(text='Thanks')
    data = await state.get_data()
    BotDB().create_user(user_id=message.from_user.id, name=data['name'], username=message.from_user.username,
                        email=data['email'], instagram=data['instagram'])
    await message.answer(text=f'Please check all your information:'
                              f'{text_user_info(data["name"], data["email"], data["instagram"])}',
                         reply_markup=callback_buttons.change_data_kb())


@router.callback_query(F.data == 'Change')
async def change_user_data(callback: types.CallbackQuery):
    await callback.message.edit_text(text=f'Selected change:', reply_markup=callback_buttons.choose_user_data_kb())
    await callback.answer()


@router.callback_query(F.data.in_({'name', 'email', 'instagram'}))
async def choose_category(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserData.data_state)
    await state.update_data(category=callback.data)
    await callback.message.edit_text(text=f'Send me your {callback.data}')
    await callback.answer()


@router.message(UserData.data_state)
async def change_selected_category(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    value = message.text
    data = await state.get_data()
    kwargs = {data['category']: value}
    BotDB().change_user_data(user_id=user_id, **kwargs)

    user = BotDB().get_user_info(message.from_user.id)
    await message.answer(text=f'Changed. Please check all your information:'
                              f'{text_user_info(user.name, user.email, user.instagram)}',
                         reply_markup=callback_buttons.change_data_kb())


@router.callback_query(F.data == 'Back change')
async def return_to_selected_category(callback: types.CallbackQuery):
    user = BotDB().get_user_info(callback.from_user.id)
    await callback.message.edit_text(text=f'Please check all your information:'
                                          f'{text_user_info(user.name, user.email, user.instagram)}',
                                     reply_markup=callback_buttons.change_data_kb())
    await callback.answer()


@router.callback_query(F.data == 'Next')
async def request_user_url_or_create_book_order(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['product'] == 'album':
        await state.set_state(UserData.url_state)
        await callback.message.edit_text(text=phrases.order_phrases["drive_link"])
    elif data['product'] == 'book':
        order_id = BotDB().create_order(user_id=callback.from_user.id, product=data['product'])
        text = BotDB().order_message_for_admin(order_id=order_id, product=data['product'])

        await sol_bot.send_message(chat_id=os.getenv('GROUP_ID'), text=f'<b>[CREATED]</b>'
                                                                       f'\n{text}')

        await callback.message.edit_text(text=f'Great! Order number: <b>{order_id}</b>')
        await callback.message.answer(text=phrases.order_phrases['book_payment'],
                                      reply_markup=callback_buttons.payment_kb())
        await state.clear()

    await callback.answer()


@router.message(UserData.url_state)
async def get_user_url(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await state.set_state(UserData.confirm_url_state)
    await message.answer(text='Please be sure about, I strongly recommend you to check it.',
                         reply_markup=callback_buttons.change_url_kb())


@router.callback_query(UserData.confirm_url_state, F.data.in_({'Next url', 'Change url'}))
async def confirm_or_change_url(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'Next url':
        url = await state.get_data()
        order_id = BotDB().create_order(user_id=callback.from_user.id, product='album', url=url['url'])
        text = BotDB().order_message_for_admin(order_id=order_id, product='album')

        await sol_bot.send_message(chat_id=os.getenv('GROUP_ID'), text=f'<b>[CREATED]</b>'
                                                                       f'\n{text}')

        await callback.message.edit_text(text=f'Great! Order number: <b>{order_id}</b>')
        await callback.message.answer(text=phrases.order_phrases['album_payment'],
                                      reply_markup=callback_buttons.payment_kb())
        await state.clear()

    if callback.data == 'Change url':
        await state.set_state(UserData.url_state)
        await callback.message.edit_text(
            text=f'No problem.'
                 f'\n\n{phrases.order_phrases["drive_link"]}')
    await callback.answer()


@router.callback_query(F.data.in_({'In Cash', 'Bank Account'}))
async def choose_payment_method(callback: types.CallbackQuery):
    if callback.data == 'In Cash':
        await callback.message.edit_text(text=phrases.order_phrases['payment_cash'])
    if callback.data == 'Bank Account':
        await callback.message.edit_text(text=phrases.order_phrases['payment_bank'])
        await callback.message.answer(text='<b>64791074681307</b>')
    await callback.message.answer(text='👌', reply_markup=default_buttons.main_menu_kb())
    await callback.answer()


def text_user_info(name, email, instagram):
    return f'\n\n<b>Name</b>: {name} ' \
           f'\n<b>Email</b>: {email} ' \
           f'\n<b>Instagram</b>: {instagram}'
