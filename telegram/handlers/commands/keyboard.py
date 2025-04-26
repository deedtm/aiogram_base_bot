from aiogram import F
from aiogram.types import Message, BotCommand
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from templates.enums.commands import Commands as tmpl
from templates.enums.exceptions import Exceptions as tmpl_ex

from ...objects import router
from ...keyboards.reply.keyboard import general
from ...states.keyboard import KeyboardState

# from .log import logger as l


@router.message(Command("keyboard"))
async def keyboard_handler(
    msg: Message, command: BotCommand, wmsg: Message, state: FSMContext
):
    await state.set_state(KeyboardState.general)
    await wmsg.delete()
    await msg.answer(tmpl.keyboard.general, reply_markup=general())


@router.message(KeyboardState.general)
async def keyboard_state(msg: Message, wmsg: Message, state: FSMContext):
    data = None
    if msg.text is not None:
        text = msg.text
    elif msg.contact is not None:
        text = "phone_number"
        data = msg.contact.phone_number
    elif msg.location is not None:
        text = "location"
        data = f"{msg.location.latitude}, {msg.location.longitude}"

    key = text.casefold().replace(" ", "_")
    template = tmpl.keyboard.__dict__.get(key, None)
    if not data:
        data = msg.from_user.__dict__.get(key, None)

    if not any((template, data)):
        await state.clear()
        await wmsg.edit_text(tmpl_ex.retry)
        return

    text = template.format(data)
    await wmsg.edit_text(text)
