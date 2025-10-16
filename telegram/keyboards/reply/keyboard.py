from aiogram.types import KeyboardButton
from .utils import build


def general():
    buttons = [
        KeyboardButton(text="ID"),
        KeyboardButton(text="Username"),
        KeyboardButton(text="First name"),
        KeyboardButton(text="Last name"),
        KeyboardButton(text="Phone number", request_contact=True),
        KeyboardButton(text="Location", request_location=True),
        KeyboardButton(text="Language code"),
        KeyboardButton(text="URL")
    ]
    return build(buttons)
