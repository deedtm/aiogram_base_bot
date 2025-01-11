from log import get_logger
from aiogram import Bot, Router
from aiogram.client.default import DefaultBotProperties
from database.utils import create_tables
from .dispatcher import BotDispatcher
from .handlers import base


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
        create_tables()
        self.logger.info(f"Starting {self.__class__.__name__}...")

        await self.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(
            self, allowed_updates=self.dp.resolve_used_update_types()
        )
