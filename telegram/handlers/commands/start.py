from aiogram.types import Message, BotCommand
from aiogram.filters import CommandStart

from templates.enums.commands import Commands as tmpl

from ...objects import router
# from .log import logger as l


@router.message(CommandStart())
async def start_handler(msg: Message, command: BotCommand, wmsg: Message):
    await wmsg.edit_text(tmpl.start)

