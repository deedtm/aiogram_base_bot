from aiogram.types import User


def get_user_identificator(user: User):
    return '@' + user.username if user.username else user.id    
    