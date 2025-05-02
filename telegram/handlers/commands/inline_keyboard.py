from typing import Optional
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config.telegram import BACK_PREFIX as BP
from templates.enums.commands import Commands as tmpl
from templates.enums.exceptions import Exceptions as tmpl_ex

from ...objects import router
from ...keyboards.inline.inline_keyboard import general
from ...keyboards.inline.__utils import back_kb as back
from ...keyboards.inline.types.extended_callback import ExtendedCallback

# from .log import logger as l


@router.message(Command("inline_keyboard"))
@router.callback_query(F.data == "ik:general")
async def ik_handler(msg: Message, wmsg: Optional[Message] = None):
    if not isinstance(msg, Message):
        wmsg = msg.message
    await wmsg.edit_text(tmpl.inline_keyboard.general, reply_markup=general())


@router.callback_query(F.data.split("<")[-1].startswith("ik"))
async def ik_callback(q: CallbackQuery):
    msg, cbd = q.message, q.data.split("<")[-1].split(":", 1)[1]
    bc = ExtendedCallback("ik:general", "General", BP)

    key = cbd.casefold().replace(" ", "_")
    template = tmpl.inline_keyboard.__dict__.get(key, None)
    data = msg.from_user.__dict__.get(key, None)

    if not any((template, data)):
        await msg.edit_text(tmpl_ex.no_data, reply_markup=back(bc))
        return

    text = template.format(data)
    await msg.edit_text(text, reply_markup=back(bc))
