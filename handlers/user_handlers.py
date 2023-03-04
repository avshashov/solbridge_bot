import os
from random import choice

from aiogram import Router, types, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv

from bot import SingleBot
from keybords import buttons
import phrases


class Loader(StatesGroup):
    upload_state = State()
    description_state = State()
    category_state = State()
    location_state = State()
    camera_state = State()
    author_state = State()
    send_state = State()
    edit_description_state = State()
    edit_category_state = State()
    edit_location_state = State()
    edit_camera_state = State()
    edit_author_state = State()


load_dotenv()
sol_bot = SingleBot()
router = Router()


# @router.channel_post()
# async def channel(message: types.Message):
#     print(message)

# @router.message()
# async def group(message: types.Message):
#     print(message)


@router.message(Command(commands=['start']))
async def start_command(message: types.Message):
    await message.answer(choice(phrases.hello_phrases), reply_markup=buttons.upload_help_kb())


@router.message(Command(commands=['help']))
async def help_command(message: types.Message):
    await message.answer(phrases.help_phrase, reply_markup=buttons.upload_help_kb())


@router.message(Text(text=['Upload photo']))
async def upload_photo(message: types.Message, state: FSMContext):
    await state.set_state(Loader.upload_state)
    await message.answer(choice(phrases.upload_photo_phrases), reply_markup=buttons.cancel_kb())


@router.message(Text(text=['Cancel']))
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Canceled', reply_markup=buttons.upload_help_kb())


@router.message(Loader.upload_state, F.content_type.in_({'photo', 'document'}))
async def get_photo(message: types.Message, state: FSMContext):
    if message.document:
        await state.update_data(file_id=message.document.file_id, file='document')
    elif message.photo:
        await state.update_data(file_id=message.photo[-1].file_id, file='photo')

    await state.set_state(Loader.description_state)
    await message.reply('Great!')
    await message.answer(choice(phrases.description_phrases))


@router.message(Loader.upload_state)
async def incorrectly_file(message: types.Message):
    await message.answer('Invalid file. Please try again', reply_markup=buttons.cancel_kb())


@router.message(Loader.description_state)
async def set_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Loader.category_state)
    await message.answer('Beautiful!')
    await message.answer(choice(phrases.category_phrases))
    await message.answer('Choose a category from the list below:', reply_markup=buttons.category_kb())


@router.callback_query(Loader.category_state, ~F.data.in_({'Confirm', 'Back'}))
async def choose_category(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data)
    await callback.message.edit_text(text=f'Selected: {callback.data}', reply_markup=buttons.confirm_kb())
    await callback.answer()


@router.callback_query(Loader.category_state)
async def confirm_category(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'Confirm':
        await state.set_state(Loader.location_state)
        category = await state.get_data()
        await callback.message.edit_text(f'Selected: {category["category"]}')
        await callback.message.answer(choice(phrases.location_phrases))
        await callback.answer()
    elif callback.data == 'Back':
        await callback.message.edit_text(text='Choose a category from the list below:',
                                         reply_markup=buttons.category_kb())
        await callback.answer()


@router.message(Loader.category_state)
async def choose_category_incorrectly(message: types.Message):
    await message.answer('Invalid category. Please try again')


@router.message(Loader.location_state)
async def set_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(Loader.camera_state)
    await message.answer(choice(phrases.camera_phrases))


@router.message(Loader.camera_state)
async def set_camera(message: types.Message, state: FSMContext):
    await state.update_data(camera=message.text)
    await state.set_state(Loader.author_state)
    await message.answer('Not bad no bad')
    await message.answer(f'{choice(phrases.artist_phrases)} (Or you can stay anonymous)',
                         reply_markup=buttons.anonymous_kb())


@router.callback_query(Loader.author_state, F.data == 'Anonymous author')
async def set_author_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(author=callback.data)
    await callback.message.answer('Check the correctness of the data')

    data = await state.get_data()
    text = text_for_message(data)
    await state.update_data(text=text)

    if data['file'] == 'document':
        await callback.message.answer_document(document=data['file_id'], caption=text)
    elif data['file'] == 'photo':
        await callback.message.answer_photo(photo=data['file_id'], caption=text)

    await state.set_state(Loader.send_state)
    await callback.message.answer('Press "Ok" to send or press "Edit" to edit message',
                                  reply_markup=buttons.ok_edit_kb())
    await callback.answer()


@router.message(Loader.author_state)
async def set_author_message(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await message.answer('Check the correctness of the data')

    data = await state.get_data()
    text = text_for_message(data)
    await state.update_data(text=text)

    if data['file'] == 'document':
        await message.answer_document(document=data['file_id'], caption=text)
    elif data['file'] == 'photo':
        await message.answer_photo(photo=data['file_id'], caption=text)

    await state.set_state(Loader.send_state)
    await message.answer('Press "Ok" to send or press "Edit" to edit message', reply_markup=buttons.ok_edit_kb())


@router.callback_query(Loader.send_state, F.data == 'Ok')
async def send_photo_to_group(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['file'] == 'document':
        await sol_bot.send_document(chat_id=os.getenv('GROUP_ID'), document=data['file_id'], caption=data['text'],
                                    reply_markup=buttons.admin_kb())
    elif data['file'] == 'photo':
        await sol_bot.send_photo(chat_id=os.getenv('GROUP_ID'), photo=data['file_id'], caption=data['text'],
                                 reply_markup=buttons.admin_kb())

    await state.clear()
    await callback.message.edit_text(text=choice(phrases.final_phrases))
    await callback.message.answer('😎', reply_markup=buttons.upload_help_kb())
    await callback.answer()


@router.callback_query(Loader.send_state, F.data == 'Edit')
async def edit_message(callback: types.CallbackQuery):
    await callback.message.edit_text(text='Select change:', reply_markup=buttons.edit_message_kb())
    await callback.answer()


@router.callback_query(F.data == '<< Back')
async def press_callback_back(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Press "Ok" to send or press "Edit" to edit message',
                                     reply_markup=buttons.ok_edit_kb())
    await state.set_state(Loader.send_state)
    await callback.answer()


@router.callback_query(F.data.in_({'Description', 'Category', 'Location', 'Camera', 'Artist'}))
async def edit_point_message(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'Description':
        await callback.message.edit_text('Write a description')
        await state.set_state(Loader.edit_description_state)

    elif callback.data == 'Category':
        await callback.message.edit_text('Choose a category', reply_markup=buttons.category_kb())
        await state.set_state(Loader.edit_category_state)

    elif callback.data == 'Location':
        await callback.message.edit_text('Write a location')
        await state.set_state(Loader.edit_location_state)

    elif callback.data == 'Camera':
        await callback.message.edit_text('Write camera')
        await state.set_state(Loader.edit_camera_state)

    elif callback.data == 'Artist':
        await callback.message.edit_text('Write the author or press "Anonymous author"',
                                         reply_markup=buttons.anonymous_kb())
        await state.set_state(Loader.edit_author_state)

    await callback.answer()


@router.message(Loader.edit_description_state)
async def edit_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Loader.send_state)
    await message.answer('Changed \nSelect new change or press "Back"', reply_markup=buttons.edit_message_kb())


@router.callback_query(Loader.edit_category_state, ~F.data.in_({'Confirm', 'Back', 'Show'}))
async def edit_category(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data)
    await callback.message.edit_text(text=f'Selected: {callback.data}', reply_markup=buttons.confirm_kb())
    await callback.answer()


@router.callback_query(Loader.edit_category_state, F.data.in_({'Confirm', 'Back'}))
async def confirm_category(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'Confirm':
        category = await state.get_data()
        await callback.message.edit_text(f'Selected: {category["category"]}', reply_markup=buttons.edit_message_kb())
        await callback.answer()
    elif callback.data == 'Back':
        await callback.message.edit_text(text='Choose a category from the list below:',
                                         reply_markup=buttons.category_kb())
        await callback.answer()


@router.message(Loader.edit_location_state)
async def edit_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(Loader.send_state)
    await message.answer('Changed \nSelect new change or press "Back"', reply_markup=buttons.edit_message_kb())


@router.message(Loader.edit_camera_state)
async def edit_camera(message: types.Message, state: FSMContext):
    await state.update_data(camera=message.text)
    await state.set_state(Loader.send_state)
    await message.answer('Changed \nSelect new change or press "Back"', reply_markup=buttons.edit_message_kb())


@router.callback_query(Loader.edit_author_state, F.data == 'Anonymous author')
async def edit_author(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(author=callback.data)
    await state.set_state(Loader.send_state)
    await callback.message.edit_text('Changed \nSelect new change or press "Back"',
                                     reply_markup=buttons.edit_message_kb())
    await callback.answer()


@router.message(Loader.edit_author_state)
async def edit_author(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(Loader.send_state)
    await message.answer('Changed \nSelect new change or press "Back"', reply_markup=buttons.edit_message_kb())


@router.callback_query(F.data == 'Show')
async def show_message(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = text_for_message(data)
    await state.update_data(text=text)

    if data['file'] == 'document':
        await callback.message.answer_document(document=data['file_id'], caption=text)
    elif data['file'] == 'photo':
        await callback.message.answer_photo(photo=data['file_id'], caption=text)
    await callback.message.answer(text='Select change:', reply_markup=buttons.edit_message_kb())
    await callback.answer()


@router.message(Text(text=['Help']))
async def help_button(message: types.Message):
    await message.answer(phrases.help_phrase, reply_markup=buttons.upload_help_kb())


def text_for_message(data: dict) -> str:
    text = f'<b>Description</b>: {data["description"]}' \
           f'\n<b>Category</b>: {data["category"]}' \
           f'\n<b>Location</b>: {data["location"]}' \
           f'\n<b>Camera</b>: {data["camera"]}' \
           f'\n<b>Artist</b>: {data["author"]}'
    return text
