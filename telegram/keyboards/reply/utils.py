from typing import Optional

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def build(buttons: list[KeyboardButton], markup: Optional[ReplyKeyboardMarkup] = None):
    b = ReplyKeyboardBuilder(markup)
    b.add(*buttons)
    b.adjust(3)
    return b.as_markup()
