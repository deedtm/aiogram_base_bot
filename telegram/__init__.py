from aiogram import Bot, Router
from aiogram.client.default import DefaultBotProperties

from .dispatcher import BotDispatcher
from .handlers import *
from config.telegram import DROP_PENDING_UPDATES
# from database.utils import create_tables
from log import get_logger


class TelegramBot(Bot):
    def __init__(
        self,
        token: str,
        router: Router,
        default_bot_properties: DefaultBotProperties = DefaultBotProperties(),
    ):
        super().__init__(token, default=default_bot_properties)
        self.dp = BotDispatcher(router)
        self.logger = get_logger(__name__)

    async def start(self):
        # create_tables()
        me = await self.me()
        self.logger.info(f"sTARTING {me.id}//{me.full_name}...")
        await self.delete_webhook(drop_pending_updates=DROP_PENDING_UPDATES)
        await self.dp.start_polling(
            self, allowed_updates=self.dp.resolve_used_update_types()
        )
