from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ...config import ACCESSES
from ...filters.access_level import AccessLevelFilter
from ...objects import router
from ...states.htmlmode import HTMLModeState


@router.message(AccessLevelFilter(ACCESSES["owner"]), Command("html_mode"))
async def htmlmode_handler(msg: Message, state: FSMContext):
    await msg.answer("✅")
    await state.set_state(HTMLModeState.general)


@router.message(AccessLevelFilter(ACCESSES["owner"]), HTMLModeState.general)
async def htmlmode_state(msg: Message):
    await msg.answer("\\n".join(msg.html_text.split("\n")).replace('"', '\\"'), parse_mode=None)
