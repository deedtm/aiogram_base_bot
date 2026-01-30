from aiogram.filters import BaseFilter
from aiogram.types import Update

from database.crud_managers import user_crud
from ..config import USERS_ACCESSES


class AccessLevelFilter(BaseFilter):
    def __init__(self, level: int):
        self.level = level

    async def __call__(self, update: Update) -> bool:
        user_id = update.from_user.id
        user = await user_crud.get_one(user_id=user_id)
        if user is None:
            user = await user_crud.add_from_tg_user(
                update.from_user, USERS_ACCESSES.get(user_id, 1)
            )
        return user.access_level >= self.level
