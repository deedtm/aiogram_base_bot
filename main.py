from dotenv import load_dotenv

load_dotenv()

import asyncio

from telegram import start_bot

if __name__ == "__main__":
    asyncio.run(start_bot())
