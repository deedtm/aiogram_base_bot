from pydantic import BaseModel

from .admin import Admin
from .inline_keyboard import InlineKeyboard
from .keyboard import Keyboard
from .quiz import Quiz
from .removeme import RemoveMe


class Commands(BaseModel):
    start: str
    database: str
    removeme: RemoveMe
    keyboard: Keyboard
    inline_keyboard: InlineKeyboard
    admin: Admin
    quiz: Quiz


__all__ = "Commands", "RemoveMe", "Keyboard", "InlineKeyboard", "Admin", "Quiz"
