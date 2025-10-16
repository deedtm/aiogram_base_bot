from aiogram.types import User as TGUser

from database.models import User as DBUser
from hyperlinks import hyperlink

from .config import CHANNEL_ID_LINK_FORMAT as CHANNEL_ID_FMT
from .config import CHANNEL_ID_POST_LINK_FORMAT as POST_ID_FMT
from .config import CHANNEL_POST_LINK_FORMAT as POST_FMT
from .config import USER_ID_LINK_FORMAT as USER_ID_FMT
from .config import USERNAME_LINK_FORMAT as USERNAME_FMT


def username_hyperlink(username: str, text: str):
    return hyperlink(USERNAME_FMT.format(username=username), text)


def user_id_hyperlink(user_id: int, text: str):
    return hyperlink(USER_ID_FMT.format(id=str(user_id)), text)


def channel_id_hyperlink(channel_id: int, text: str):
    return hyperlink(CHANNEL_ID_FMT.format(id=channel_id), text)


def post_hyperlink(username: str, post_id: int, text: str):
    return hyperlink(POST_FMT.format(username=username, post_id=post_id), text)


def post_id_hyperlink(channel_id: int, post_id: int, text: str):
    return hyperlink(POST_ID_FMT.format(id=channel_id, post_id=post_id), text)


def user_hyperlink(user: TGUser | DBUser):
    text = user.first_name
    if user.last_name:
        text += " " + user.last_name
    if user.username:
        return username_hyperlink(user.username, text)
    else:
        return user_id_hyperlink(user.id, text)
