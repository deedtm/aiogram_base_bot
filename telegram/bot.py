from aiogram import Bot, Router
from loguru import logger

from database.utils import init_schemas

from .config import DROP_PENDING_UPDATES, DEFAULT_BOT_PROPERTIES
from .dispatcher import BotDispatcher
from .handlers import *


class TelegramBot(Bot):
    def __init__(self, token: str, router: Router):
        super().__init__(token, default=DEFAULT_BOT_PROPERTIES)
        self.dp = BotDispatcher(router)

    async def start(self):
        await init_schemas()

        me = await self.me()
        logger.info(f"sTARTING {me.id}:{me.full_name}...")
        await self.delete_webhook(drop_pending_updates=DROP_PENDING_UPDATES)
        await self.dp.start_polling(
            self, allowed_updates=self.dp.resolve_used_update_types()
        )
