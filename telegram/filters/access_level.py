from aiogram.filters import BaseFilter
from aiogram.types import Update

from database.utils import get_user


class AccessLevelFilter(BaseFilter):
    def __init__(self, level: int):
        self.level = level

    async def __call__(self, update: Update) -> bool:
        user_id = update.from_user.id
        user = await get_user(user_id)
        if user is None:
            return False
        return user.access_level >= self.level
