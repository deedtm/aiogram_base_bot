from aiogram.filters import Command
from aiogram.types import Message

from database.crud_managers import user_crud
from templates import COMMANDS as tmpl

from ...objects import router


@router.message(Command("database"))
async def database_handler(msg: Message, wmsg: Message):
    dbuser = await user_crud.get_one(user_id=msg.from_user.id)
    parsed = []
    for key, value in dbuser.as_dict.items():
        field = key.replace("_", " ").title()
        parsed.append(f"<b>{field}</b>: {value}")

    text = tmpl.database.format("\n".join(parsed))
    await wmsg.edit_text(text)
