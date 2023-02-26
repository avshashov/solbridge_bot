from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def upload_photo_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Upload photo")
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=False)


def cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Cancel")
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=False)


def ok_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Ok")
    kb.button(text="Cancel")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=False)


def category_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="What is South Korea for me",
                              callback_data="What is South Korea for me")],
        [InlineKeyboardButton(text="The purest feeling in the life",
                              callback_data="The purest feeling in the life")],
        [InlineKeyboardButton(text="Student’s life",
                              callback_data="Student’s life"),
         InlineKeyboardButton(text="Urban",
                              callback_data="Urban")],
        [InlineKeyboardButton(text="Model photography",
                              callback_data="Model photography"),
         InlineKeyboardButton(text="People",
                              callback_data="People")],
        [InlineKeyboardButton(text="Creativity",
                              callback_data="Creativity"),
         InlineKeyboardButton(text="Nature",
                              callback_data="Nature")],
        [InlineKeyboardButton(text="Global citizen",
                              callback_data="Global citizen")]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
