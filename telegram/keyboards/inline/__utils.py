from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .types.ibutton import IButton
from .types.extended_callback import ExtendedCallback


def build(
    buttons: Optional[list[IButton]] = None,
    markup: Optional[InlineKeyboardMarkup] = None,
    add_back: bool = False,
) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder(markup)
    b.add(*[ib.to_ikb() for ib in buttons])
    b.adjust(3)
    ik = b.export()

    if add_back:
        added = []
        for ib in buttons:
            if not ib.back_callback or ib.back_callback in added:
                continue
            ec = ib.back_callback
            ik.append(
                [InlineKeyboardButton(text=ec.prefix_text(), callback_data=ec.data)]
            )
            added.append(ec)

    return InlineKeyboardMarkup(inline_keyboard=ik)


def back_kb(back_callback: ExtendedCallback) -> InlineKeyboardMarkup:
    bc = back_callback
    b = InlineKeyboardBuilder()
    b.add(InlineKeyboardButton(text=bc.prefix_text(), callback_data=bc.data))
    return b.as_markup()
