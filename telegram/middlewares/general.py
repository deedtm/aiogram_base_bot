from html import escape
from traceback import format_exc
from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message, CallbackQuery, Update

from database.utils import add_user
from templates.enums.middlewares import Middlewares as tmpl_mw
from templates.enums.exceptions import Exceptions as tmpl_ex

from ..enums.middlewares import Middlewares
from ..log import l


class GeneralMW(BaseMiddleware):
    def __init__(self) -> None: ...

    async def wrapper(
        self,
        handler: Callable,
        event: Update,
        data: dict,
        wmsg: Optional[Message] = None,
    ) -> Any:
        err = None
        ok = False
        try:
            if isinstance(event, Message):
                await add_user(event.from_user)
            await handler(event, data)
            ok = True
        except TelegramAPIError as e:
            err = e
            if "message is not modified" in e.message:
                ok = True
                return
            l.error(f"Telegram API error: {e}")
        except Exception as e:
            err = e
            l.error(format_exc())
        finally:
            if not ok:
                text = tmpl_ex.base.format(escape(str(err)))
                if isinstance(wmsg, Message):
                    await wmsg.edit_text(text)
                else:
                    await event.bot.send_message(event.message.chat.id, text)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        is_callback = isinstance(event, CallbackQuery)
        wmsg = await event.answer(tmpl_mw.wait_message)

        if not is_callback:
            context = data["state"]
            state = await context.get_state()
            if state is not None and event.text.startswith("/"):
                await context.clear()
                await wmsg.edit_text(tmpl_ex.retry)
                return

            params = data["handler"].params
            for lit in Middlewares.WAIT_MESSAGE_LITERALS:
                if lit in params:
                    data[lit] = wmsg
                    break

        return await self.wrapper(handler, event, data, wmsg)
