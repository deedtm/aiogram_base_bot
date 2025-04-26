from config.telegram import BACK_PREFIX as BP

from .types.ibutton import IButton
from .types.extended_callback import ExtendedCallback as EC
from .utils import build, back_kb


def general():
    bc = EC("ik:general", "General", BP)
    buttons = [
        IButton(text="ID", callback_data="ik:id", back_callback=bc),
        IButton(text="Username", callback_data="ik:username", back_callback=bc),
        IButton(text="First name", callback_data="ik:first_name", back_callback=bc),
        IButton(text="Last name", callback_data="ik:last_name", back_callback=bc),
        IButton(text="Language code", callback_data="ik:language_code", back_callback=bc),
        IButton(text="URL", callback_data="ik:url", back_callback=bc),
    ]
    return build(buttons)


def back(back_callback: EC):
    return back_kb(back_callback)
