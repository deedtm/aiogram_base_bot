from asyncio import sleep

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.crud_managers import user_crud
from templates import COMMANDS as tmpl
from templates import EXCEPTIONS as tmpl_ex

from ...objects import router
from ...states.quiz import QuizState

t = tmpl.quiz


STEPS = ["color", "food", "work", "pet"]


@router.message(Command("quiz"))
async def quiz_start_handler(msg: Message, wmsg: Message, state: FSMContext):
    await wmsg.edit_text(t.start)
    await state.set_state(QuizState.input)
    await sleep(0.5)
    await msg.answer(t.color)
    await state.update_data(step_index=0, answers={})


@router.message(QuizState.input)
async def quiz_input_handler(msg: Message, state: FSMContext):
    if msg.text is None:
        await msg.answer(tmpl_ex.no_args)
        return

    data = await state.get_data()
    step_index = data.get("step_index", 0)
    next_step_index = step_index + 1
    answers = data.get("answers", {})
    answers[STEPS[step_index]] = msg.text
    await state.update_data(answers=answers, step_index=next_step_index)

    if next_step_index >= len(STEPS):
        await quiz_end(msg, state)
        return

    await msg.answer(getattr(tmpl.quiz, STEPS[next_step_index]))


async def quiz_end(msg: Message, state: FSMContext):
    data = await state.get_data()
    answers = data.get("answers", {})

    db_data = {"favorite_" + k: v for k, v in answers.items()}
    await user_crud.update("user_id", msg.from_user.id, **db_data)

    await msg.answer(
        t.end.format(
            answers.get("color", "N/A"),
            answers.get("food", "N/A"),
            answers.get("work", "N/A"),
            answers.get("pet", "N/A"),
        )
    )
    await state.clear()
