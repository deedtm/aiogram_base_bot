from pydantic import BaseModel

from .admin import Admin
from .inline_keyboard import InlineKeyboard
from .keyboard import Keyboard
from .removeme import RemoveMe


class Commands(BaseModel):
    start: str
    database: str
    removeme: RemoveMe
    keyboard: Keyboard
    inline_keyboard: InlineKeyboard
    admin: Admin


__all__ = "Commands", "RemoveMe", "Keyboard", "InlineKeyboard", "Admin"
