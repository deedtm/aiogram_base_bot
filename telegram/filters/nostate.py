from aiogram import types
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext


class NoState(BaseFilter):
    async def __call__(self, message: types.Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        return current_state is None
