from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Upload photo')
    kb.button(text='Photo Album')
    kb.button(text='Order a book')
    kb.button(text='Help')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Cancel')
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=False)


def cancel_order_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Cancel the order')
    kb.button(text='Cancel')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=False)
