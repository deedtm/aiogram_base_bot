from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

from templates.enums.messages import Messages as tmpl

from .log import logger
from ...utils import get_username_or_user_id
from ...objects import router
from ...filters.nostate import NoState


@router.message(NoState(), ~F.text.startswith("/"))
async def message_handler(msg: Message, wmsg: Message):
    identificator = get_username_or_user_id(msg.from_user)
    logger.info(msg=f"Got message from {identificator}")

    if msg.text:
        await wmsg.edit_text(tmpl.text.format(msg.text))
        return

    text = tmpl.media.format(" ".join(msg.content_type.lower().split("_")))
    await wmsg.edit_text(text)
