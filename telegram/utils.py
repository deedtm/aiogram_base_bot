from aiogram.types import User as TGUser
from database.models import User as DBUser
from database.utils import get_access_level


def get_user_identificator(user: TGUser):
    return "@" + user.username if user.username else user.id


def get_user_hyperlink(user: TGUser | DBUser):
    link_fmt = '<a href="{link}">{text}</a>'
    text = user.first_name
    if user.last_name:
        text += " " + user.last_name
    if user.username:
        link = f"https://t.me/{user.username}"
    else:
        link = f"tg://user?id={user.id}"

    return link_fmt.format(link=link, text=text)
