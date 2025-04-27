from aiogram.types import Message
from aiogram.filters import Command

from database.utils import get_user_data
from templates.enums.commands import Commands as tmpl

from ...objects import router


@router.message(Command("database"))
async def database_handler(msg: Message, wmsg: Message):
    dbuser = await get_user_data(msg.from_user.id)
    parsed = []
    for key, value in dbuser.items():
        field = key.replace('_', ' ').title()
        parsed.append(f"<b>{field}</b>: {value}")
    
    text = tmpl.database.format('\n'.join(parsed))
    await wmsg.edit_text(text)
