from aiogram.types import InlineKeyboardButton
from .extended_callback import ExtendedCallback


class IButton(InlineKeyboardButton):
    def __init__(
        self,
        *,
        text: str,
        callback_data: str = None,
        back_callback: ExtendedCallback = None,
        url: str = None,
        web_app: str = None,
        login_url: str = None,
        switch_inline_query: str = None,
        switch_inline_query_current_chat: str = None,
        callback_game: str = None,
        pay: bool = None,
        **pydantic_kwargs,
    ):
        super().__init__(
            text=text,
            callback_data=callback_data,
            url=url,
            web_app=web_app,
            login_url=login_url,
            switch_inline_query=switch_inline_query,
            switch_inline_query_current_chat=switch_inline_query_current_chat,
            callback_game=callback_game,
            pay=pay,
            **pydantic_kwargs,
        )
        self.text = text
        self.callback_data = callback_data
        self.back_callback = back_callback
        self.url = url
        self.web_app = web_app
        self.login_url = login_url
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        self.pay = pay

    def from_ikb(button: InlineKeyboardButton):
        cb = button.callback_data
        back_cb = None
        if "<" in cb:
            back_start, back_end = cb.find("<"), cb.rfind("<")
            back_cb_data = cb[back_start + 1 : back_end]
            cb = cb[:back_start] + cb[back_end + 1 :]
            text = back_cb_data.replace("_", " ").title()
            back_cb = ExtendedCallback(back_cb_data, text)

        return IButton(
            text=button.text,
            callback_data=cb,
            back_callback=back_cb,
            url=button.url,
            web_app=button.web_app,
            login_url=button.login_url,
            switch_inline_query=button.switch_inline_query,
            switch_inline_query_current_chat=button.switch_inline_query_current_chat,
            callback_game=button.callback_game,
            pay=button.pay,
        )

    def to_ikb(self) -> InlineKeyboardButton:
        callback_data = self.callback_data
        if self.back_callback:
            callback_data = "<" + self.back_callback.data + "<" + callback_data

        return InlineKeyboardButton(
            text=self.text,
            callback_data=callback_data,
            url=self.url,
            web_app=self.web_app,
            login_url=self.login_url,
            switch_inline_query=self.switch_inline_query,
            switch_inline_query_current_chat=self.switch_inline_query_current_chat,
            callback_game=self.callback_game,
            pay=self.pay,
        )
