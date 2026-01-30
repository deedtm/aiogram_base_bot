from aiogram.fsm.state import State, StatesGroup


class QuizState(StatesGroup):
    input = State("quiz:input")
