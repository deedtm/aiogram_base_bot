from aiogram.types import User as TGUser


def get_username_or_user_id(user: TGUser):
    return "@" + user.username if user.username else user.id
