from aiogram import F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from database.utils import delete_user
from templates import COMMANDS as tmpl

from ...keyboards.inline.removeme import kb
from ...objects import router


@router.message(Command("removeme"))
async def removeme_handler(msg: Message, wmsg: Message):
    await wmsg.edit_text(tmpl.removeme.general, reply_markup=kb())


@router.callback_query(F.data == "rm:yes")
async def removeme_callback(q: CallbackQuery):
    await delete_user(q.from_user.id)
    await q.message.edit_text(tmpl.removeme.yes, reply_markup=None)
