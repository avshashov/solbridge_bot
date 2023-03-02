from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def upload_help_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Upload photo")
    kb.button(text="Help")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=False)


def cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Cancel")
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=False)


def edit_message_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Description", callback_data="Description"),
            InlineKeyboardButton(text="Category", callback_data="Category")
        ],
        [
            InlineKeyboardButton(text="Location", callback_data="Location"),
            InlineKeyboardButton(text="Camera", callback_data="Camera")
        ],
        [
            InlineKeyboardButton(text="Artist", callback_data="Artist")
        ],
        [
            InlineKeyboardButton(text="<< Back to post", callback_data="<< Back"),
            InlineKeyboardButton(text="Show message", callback_data="Show")
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
            InlineKeyboardButton(text="What is South Korea for me", callback_data="What is South Korea for me")
        ],
        [
            InlineKeyboardButton(text="The purest feeling in the life",
                                 callback_data="The purest feeling in the life")
        ],
        [
            InlineKeyboardButton(text="Student’s life", callback_data="Student’s life"),
            InlineKeyboardButton(text="Urban", callback_data="Urban")
        ],
        [
            InlineKeyboardButton(text="Model photography", callback_data="Model photography"),
            InlineKeyboardButton(text="People", callback_data="People")
        ],
        [
            InlineKeyboardButton(text="Creativity", callback_data="Creativity"),
            InlineKeyboardButton(text="Nature", callback_data="Nature")
        ],
        [
            InlineKeyboardButton(text="Global citizen", callback_data="Global citizen")
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
