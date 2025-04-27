from .types.ibutton import IButton
from .utils import build


def kb():
    buttons = [
        IButton(text="✅  I'm surely sure 💯💯💯", callback_data="rm:yes"),
    ]
    return build(buttons)

