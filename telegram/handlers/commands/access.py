from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message

from database.crud_managers import user_crud
from templates import COMMANDS as tmpl
from templates import EXCEPTIONS as tmpl_ex

from ...config import ACCESSES
from ...filters.access_level import AccessLevelFilter
from ...objects import router


@router.message(AccessLevelFilter(ACCESSES["admin"]), Command("access"))
async def access_handler(msg: Message, command: CommandObject, wmsg: Message):
    if not command.args:
        text = tmpl_ex.no_args
        await wmsg.edit_text(text)
        return

    args = command.args.split()

    if len(args) != 2 or not all(arg.isdigit() for arg in args):
        text = tmpl_ex.wrong_args
        await wmsg.edit_text(text)
        return

    sender = await user_crud.get_one(user_id=msg.from_user.id)

    user_id, access_level = map(int, args)
    user = await user_crud.get_one(user_id=user_id)

    if not user:
        await wmsg.edit_text(tmpl_ex.user_not_found)
        return

    if user.user_id == msg.from_user.id:
        await wmsg.edit_text(tmpl_ex.own_access)
        return

    if user.access_level >= sender.access_level:
        await wmsg.edit_text(tmpl_ex.low_access_to_set)
        return

    if access_level >= sender.access_level:
        await wmsg.edit_text(tmpl_ex.over_access_set)
        return

    await user_crud.update("user_id", user_id, access_level=access_level)

    full_name = (user.first_name + " " + (user.last_name or "")).strip()
    text = tmpl.admin.access.format(user.access_level, access_level, full_name)
    await wmsg.edit_text(text)
