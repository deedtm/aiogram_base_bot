from aiogram.filters import Command
from aiogram.types import Message

from database.utils import get_user
from templates import COMMANDS as tmpl

from ...enums.commands import parse_commands
from ...filters.access_level import AccessLevelFilter
from ...objects import router


@router.message(AccessLevelFilter(2), Command("admin"))
async def admin_handler(msg: Message, wmsg: Message):
    user = await get_user(msg.from_user.id)
    parsed = parse_commands(tmpl.admin.commands_list_fmt, user.access_level)
    text = tmpl.admin.general.format("\n".join(parsed))
    await wmsg.edit_text(text)
