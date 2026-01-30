from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message

from database.crud_managers import user_crud
from templates import COMMANDS as tmpl
from templates import EXCEPTIONS as tmpl_ex

from ...config import ACCESSES
from ...filters.access_level import AccessLevelFilter
from ...objects import router


@router.message(AccessLevelFilter(ACCESSES["moderator"]), Command("getuser"))
async def getuser_handler(msg: Message, command: CommandObject, wmsg: Message):
    if not command.args:
        text = tmpl_ex.no_args
        await wmsg.edit_text(text)
        return

    try:
        user_id = int(command.args)
    except ValueError:
        text = tmpl_ex.wrong_args
        await wmsg.edit_text(text)
        return

    dbuser = await user_crud.get_one(user_id=user_id)
    parsed = []
    for key, value in dbuser.as_dict.items():
        field = key.replace("_", " ").capitalize()
        parsed.append(tmpl.admin.user_fmt.format(field, value))

    text = tmpl.admin.getuser.format("\n".join(parsed))
    await wmsg.edit_text(text)
