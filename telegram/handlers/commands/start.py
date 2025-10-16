from aiogram.filters import CommandStart
from aiogram.types import BotCommand, Message

from templates import COMMANDS as tmpl

from ...objects import router


@router.message(CommandStart())
async def start_handler(msg: Message, command: BotCommand, wmsg: Message):
    await wmsg.edit_text(tmpl.start)
