from aiogram.types import Message
from aiogram.filters import Command

from database.utils import get_access_level
from templates.enums.commands import Commands as tmpl

from ...filters.access_level import AccessLevelFilter
from ...enums.commands import parse_commands
from ...objects import router


@router.message(AccessLevelFilter(2), Command("admin"))
async def admin_handler(msg: Message, wmsg: Message):
    access = await get_access_level(msg.from_user.id)
    parsed = parse_commands(tmpl.admin.commands_list_fmt, access)
    text = tmpl.admin.general.format("\n".join(parsed))
    await wmsg.edit_text(text)
