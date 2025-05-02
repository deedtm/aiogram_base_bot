from aiogram.fsm.state import State, StatesGroup


class UsersState(StatesGroup):
    search = State('getuser:general')
