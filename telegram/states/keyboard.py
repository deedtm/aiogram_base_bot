from aiogram.fsm.state import State, StatesGroup


class KeyboardState(StatesGroup):
    general = State('keyboard:general')
       