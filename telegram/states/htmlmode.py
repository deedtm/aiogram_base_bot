from aiogram.fsm.state import State, StatesGroup


class HTMLModeState(StatesGroup):
    general = State("htmlm:general")
