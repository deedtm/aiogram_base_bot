from aiogram.types import Message
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext

from database.utils import get_user_data
from templates.enums.commands import Commands as tmpl
from templates.enums.exceptions import Exceptions as tmpl_ex

from ...filters.access_level import AccessLevelFilter
from ...objects import router
from ...states.users import UsersState


@router.message(AccessLevelFilter(2), Command("getuser"))
async def getuser_handler(msg: Message, command: CommandObject, wmsg: Message):
    if not command.args:
        text = tmpl_ex.no_args
        await wmsg.edit_text(text)
        return
    
    dbuser = await get_user_data(int(command.args))
    parsed = []
    for key, value in dbuser.items():
        field = key.replace("_", " ").capitalize()
        parsed.append(tmpl.admin.user_fmt.format(field, value))

    text = tmpl.admin.getuser.format("\n".join(parsed))
    await wmsg.edit_text(text)
