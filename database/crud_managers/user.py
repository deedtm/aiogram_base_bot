from datetime import datetime
from html import escape

from aiogram.types import User as TgUser

from ..models import User
from .base import CRUDBase


class UserCRUD(CRUDBase[User]):
    model = User

    async def add_from_tg_user(self, tg_user: TgUser, access_level: int = 1) -> User:
        existing = await self.get_one(user_id=tg_user.id)
        if existing:
            return existing
        fields = {
            "user_id": tg_user.id,
            "username": tg_user.username,
            "first_name": escape(tg_user.first_name),
            "last_name": escape(tg_user.last_name) if tg_user.last_name else None,
            "register_date": int(datetime.now().timestamp()),
            "access_level": access_level,
        }
        new_user = await self.add(**fields)
        return new_user
