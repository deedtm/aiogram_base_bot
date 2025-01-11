from database.utils import *
from aiogram.types import Message


async def handler(msg: Message):
    is_user = is_user_in(msg.from_user.id)
    if is_user:
        await msg.answer("Welcome back! You are already registered.")
    else:
        add_user(msg.from_user)
        await msg.answer("Welcome! You have been successfully registered.")

    user_details = get_user(msg.from_user.id)
    await msg.answer(f"Your details:\n- {'\n- '.join(map(str, user_details))}")
