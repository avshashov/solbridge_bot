from aiogram import Router, types, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keybords import buttons


class Loader(StatesGroup):
    upload_state = State()
    filename_state = State()
    category_state = State()
    location_state = State()
    camera_state = State()
    author_state = State()
    send_state = State()


categories = [
    'What is South Korea for me',
    'Student’s life',
    'The purest feeling in the life',
    'Urban',
    'Model photography',
    'People',
    'Creativity',
    'Nature',
    'Global citizen'
]

router = Router()


@router.message(Command(commands=['start']))
async def start_command(message: types.Message):
    await message.answer('Hello. This is a test bot!', reply_markup=buttons.upload_photo_kb())


@router.message(Text(text=['Upload photo']))
async def upload_photo(message: types.Message, state: FSMContext):
    await state.set_state(Loader.upload_state)
    await message.answer('send a photo as a document', reply_markup=buttons.cancel_kb())


@router.message(Text(text=['Cancel']))
async def cancel(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Canceled', reply_markup=buttons.upload_photo_kb())


@router.message(Loader.upload_state, F.document)
async def get_photo(message: types.Message, state: FSMContext):
    await state.update_data(file_id=message.document.file_id)
    await state.set_state(Loader.filename_state)
    await message.answer('Write the name of the photo')


@router.message(Loader.upload_state)
async def incorrectly_file(message: types.Message) -> None:
    await message.answer('Invalid file. Please try again', reply_markup=buttons.cancel_kb())


@router.message(Loader.filename_state)
async def set_filename(message: types.Message, state: FSMContext):
    await state.update_data(filename=message.text)
    await state.set_state(Loader.category_state)
    await message.answer('Choose a category')


@router.message(Loader.category_state, F.text.in_(categories))
async def choose_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(Loader.location_state)
    await message.answer('Write a location')


@router.message(Loader.category_state)
async def choose_category_incorrectly(message: types.Message):
    await message.answer('Invalid category. Please try again')


@router.message(Loader.location_state)
async def set_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(Loader.camera_state)
    await message.answer('Write camera model')


@router.message(Loader.camera_state)
async def set_location(message: types.Message, state: FSMContext):
    await state.update_data(camera=message.text)
    await state.set_state(Loader.author_state)
    await message.answer('Write the author')


@router.message(Loader.author_state)
async def set_location(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await message.answer('Check the correctness of the data')

    data = await state.get_data()
    text = f'Description: {data["filename"]}' \
           f'\nCategory: {data["category"]}' \
           f'\nLocation: {data["location"]}' \
           f'\nCamera: {data["camera"]}' \
           f'\nArtist: {data["author"]}'
    await message.answer_document(document=data["file_id"], caption=text)

    await state.set_state(Loader.send_state)
    await message.answer('Press Ok to send', reply_markup=buttons.ok_cancel_kb())


@router.message(Loader.send_state)
async def send_photo_to_channel(message: types.Message, state: FSMContext):
    # await message.answer_document(document=message.document.file_id, caption='some text')
    await state.clear()
    await message.answer('Done', reply_markup=buttons.upload_photo_kb())
