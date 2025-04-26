import asyncio
import logging
import templates
from telegram import TelegramBot
from config.telegram import TOKEN, PARSE_MODE, DISABLE_LINK_PREVIEW
from log.utils import disable_loggers
from aiogram.client.default import DefaultBotProperties
from telegram.objects import router


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    disable_loggers("aiogram")

    default = DefaultBotProperties(
        parse_mode=PARSE_MODE, link_preview_is_disabled=DISABLE_LINK_PREVIEW
    )
    bot = TelegramBot(TOKEN, router, default)
    asyncio.run(bot.start())
