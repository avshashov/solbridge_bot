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


router = Router()


@router.message(Command(commands=['start']))
async def start_command(message: types.Message):
    await message.answer('Hello! I am PCS_Bot, and I will help you to share your piece of art with people! 😎',
                         reply_markup=buttons.upload_photo_kb())


@router.message(Text(text=['Upload photo']))
async def upload_photo(message: types.Message, state: FSMContext):
    await state.set_state(Loader.upload_state)
    await message.answer('For beginning, show me your photo', reply_markup=buttons.cancel_kb())


@router.message(Text(text=['Cancel']))
async def cancel(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Canceled', reply_markup=buttons.upload_photo_kb())


@router.message(Loader.upload_state, F.content_type.in_({'photo', 'document'}))
async def get_photo(message: types.Message, state: FSMContext):
    if message.document:
        await state.update_data(file_id=message.document.file_id, file='document')
    elif message.photo:
        await state.update_data(file_id=message.photo[-1].file_id, file='photo')

    await state.set_state(Loader.filename_state)
    await message.reply('Great!')
    await message.answer('I think, we should give the name of this piece of art ')


@router.message(Loader.upload_state)
async def incorrectly_file(message: types.Message) -> None:
    await message.answer('Invalid file. Please try again', reply_markup=buttons.cancel_kb())


@router.message(Loader.filename_state)
async def set_filename(message: types.Message, state: FSMContext):
    await state.update_data(filename=message.text)
    await state.set_state(Loader.category_state)
    await message.answer('Beatiful!')
    await message.answer('Choose a category from the list below:', reply_markup=buttons.category_kb())


@router.callback_query(Loader.category_state)
async def choose_category(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data)
    await state.set_state(Loader.location_state)
    await callback.message.answer('Where did you take a photo?')
    await callback.answer()


@router.message(Loader.category_state)
async def choose_category_incorrectly(message: types.Message):
    await message.answer('Invalid category. Please try again')


@router.message(Loader.location_state)
async def set_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(Loader.camera_state)
    await message.answer('What is the camera helped you did it?')


@router.message(Loader.camera_state)
async def set_location(message: types.Message, state: FSMContext):
    await state.update_data(camera=message.text)
    await state.set_state(Loader.author_state)
    await message.answer('Not bad no bad')
    await message.answer('Now, could you tell me, who made this shot? (Or you can stay anonymous)')


@router.message(Loader.author_state)
async def set_location(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await message.answer('Check the correctness of the data')

    data = await state.get_data()
    text = f'<b>Description</b>: {data["filename"]}' \
           f'\n<b>Category</b>: {data["category"]}' \
           f'\n<b>Location</b>: {data["location"]}' \
           f'\n<b>Camera</b>: {data["camera"]}' \
           f'\n<b>Artist</b>: {data["author"]}'
    if data['file'] == 'document':
        await message.answer_document(document=data["file_id"], caption=text)
    elif data['file'] == 'photo':
        await message.answer_photo(photo=data["file_id"], caption=text)

    await state.set_state(Loader.send_state)
    await message.answer('Press Ok to send', reply_markup=buttons.ok_cancel_kb())


@router.message(Loader.send_state)
async def send_photo_to_channel(message: types.Message, state: FSMContext):
    # await message.answer_document(document=message.document.file_id, caption='some text')
    await state.clear()
    await message.answer('Done', reply_markup=buttons.upload_photo_kb())
