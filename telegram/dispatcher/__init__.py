from aiogram import Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage


class BotDispatcher(Dispatcher):
    def __init__(self, router: Router):
        super().__init__(storage=MemoryStorage())
        self.include_router(router)
    