from dotenv import load_dotenv

load_dotenv()

import asyncio

from loguru import logger

logger.add(
    "logs/debug.log",
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    level="DEBUG",
)

from telegram import start_bot

if __name__ == "__main__":
    asyncio.run(start_bot())
