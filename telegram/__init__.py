from .bot import TelegramBot
from .config import TOKEN
from .objects import router

bot_instance = TelegramBot(TOKEN, router)


async def start_bot():
    await bot_instance.start()
