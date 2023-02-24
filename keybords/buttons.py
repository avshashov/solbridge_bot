from aiogram.types import ReplyKeyboardMarkup
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
