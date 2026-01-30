from html import escape
from traceback import format_exc
from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery, Message, Update, User
from loguru import logger as l

from database.crud_managers import user_crud
from templates import EXCEPTIONS as tmpl_ex
from templates import MIDDLEWARES as tmpl_mw

from ..config import USERS_ACCESSES
from ..enums.middlewares import Middlewares


class GeneralMW(BaseMiddleware):
    def __init__(self) -> None: ...

    async def _parse_user(self, event: Update):
        from_user = getattr(event, "from_user", None)
        if not from_user and (message := getattr(event, "message", None)):
            from_user = getattr(message, "from_user", None)
        return from_user

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
            u = await self._parse_user(event)
            if isinstance(u, User):
                await user_crud.add_from_tg_user(u, USERS_ACCESSES.get(u.id, 1))

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
        wmsg = None

        if not is_callback:
            params = data["handler"].params
            wmsg_literal = None
            for lit in Middlewares.WAIT_MESSAGE_LITERALS:
                if lit in params:
                    wmsg_literal = lit
                    break

            if wmsg_literal is not None:
                wmsg = await event.answer(tmpl_mw.wait_message)
                data[wmsg_literal] = wmsg

            context = data["state"]
            state = await context.get_state()
            if state is not None and event.text and event.text.startswith("/"):
                await context.clear()
                if wmsg_literal is not None:
                    await wmsg.edit_text(tmpl_ex.retry)
                else:
                    await event.answer(tmpl_ex.retry)
                return

        return await self.wrapper(handler, event, data, wmsg)
