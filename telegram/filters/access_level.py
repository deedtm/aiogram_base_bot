from aiogram.types import Update
from aiogram.filters import BaseFilter

from database.utils import get_access_level


class AccessLevelFilter(BaseFilter):
    def __init__(self, level: int):
        self.level = level

    async def __call__(self, update: Update) -> bool:
        user_id = update.from_user.id
        access = await get_access_level(user_id)
        return access >= self.level
