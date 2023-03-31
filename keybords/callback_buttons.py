from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from solbot_db.db_orm import BotDB


def edit_message_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='Description', callback_data='Description'),
            InlineKeyboardButton(text='Category', callback_data='Category')
        ],
        [
            InlineKeyboardButton(text='Location', callback_data='Location'),
            InlineKeyboardButton(text='Camera', callback_data='Camera')
        ],
        [
            InlineKeyboardButton(text='Artist', callback_data='Artist')
        ],
        [
            InlineKeyboardButton(text='<< Back to post', callback_data='<< Back'),
            InlineKeyboardButton(text='Show message', callback_data='Show')
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def ok_edit_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Ok', callback_data='Ok'))
    builder.add(InlineKeyboardButton(text='Edit', callback_data='Edit'))
    return builder.as_markup()


def category_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='What is South Korea for me', callback_data='What is South Korea for me')
        ],
        [
            InlineKeyboardButton(text='The purest feeling in the life',
                                 callback_data='The purest feeling in the life')
        ],
        [
            InlineKeyboardButton(text="Student’s life", callback_data="Student’s life"),
            InlineKeyboardButton(text='Urban', callback_data='Urban')
        ],
        [
            InlineKeyboardButton(text='Model photography', callback_data='Model photography'),
            InlineKeyboardButton(text='People', callback_data='People')
        ],
        [
            InlineKeyboardButton(text='Creativity', callback_data='Creativity'),
            InlineKeyboardButton(text='Nature', callback_data='Nature')
        ],
        [
            InlineKeyboardButton(text='Global citizen', callback_data='Global citizen')
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def confirm_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Confirm selection', callback_data='Confirm'))
    builder.add(InlineKeyboardButton(text='Back', callback_data='Back'))
    builder.adjust(1)
    return builder.as_markup()


def anonymous_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Anonymous author', callback_data='Anonymous author'))
    return builder.as_markup()


def admin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Publish', callback_data='Publish'))
    builder.add(InlineKeyboardButton(text='Reject', callback_data='Reject'))
    return builder.as_markup()


def yes_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Yes', callback_data='Yes'))
    builder.add(InlineKeyboardButton(text='Back to main menu', callback_data='Main menu'))
    return builder.as_markup()


def change_data_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Continue', callback_data='Next'))
    builder.add(InlineKeyboardButton(text='Edit', callback_data='Change'))
    return builder.as_markup()


def choose_user_data_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Name', callback_data='name'))
    builder.add(InlineKeyboardButton(text='Email', callback_data='email'))
    builder.add(InlineKeyboardButton(text='Instagram', callback_data='instagram'))
    builder.add(InlineKeyboardButton(text='Back', callback_data='Back change'))
    builder.adjust(1)
    return builder.as_markup()


def change_url_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Everything is cool', callback_data='Next url'))
    builder.add(InlineKeyboardButton(text='Edit a link', callback_data='Change url'))
    return builder.as_markup()


def order_photo_album_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Order the Photo Album', callback_data='album'))
    return builder.as_markup()


def order_book_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Order the PCS Book', callback_data='book'))
    return builder.as_markup()


def payment_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='In Cash', callback_data='In Cash'))
    builder.add(InlineKeyboardButton(text='Bank Account', callback_data='Bank Account'))
    return builder.as_markup()


def unpaid_orders_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    unpaid_orders = BotDB().get_unpaid_orders()

    for order in unpaid_orders:
        builder.add(InlineKeyboardButton(text=order[0], callback_data=f'order {order[0]}'))

    builder.adjust(1)
    return builder.as_markup()


def order_unpaid_more_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='✅ Approve the order', callback_data='Approve'))
    builder.add(InlineKeyboardButton(text='❌ Cancel the order', callback_data='Cancel'))
    builder.add(InlineKeyboardButton(text='↩️ Back to orders', callback_data='Back to orders'))
    builder.adjust(2)
    return builder.as_markup()
