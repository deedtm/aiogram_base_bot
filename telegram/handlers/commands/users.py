from aiogram import F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.crud_managers import User, user_crud
from templates import COMMANDS as tmpl
from templates import EXCEPTIONS as tex

from ...config import ACCESSES
from ...config import USERS_LIST_AMOUNT as USERS_AMOUNT
from ...filters.access_level import AccessLevelFilter
from ...hyperlinks import user_hyperlink
from ...keyboards.inline.users import kb
from ...objects import router
from ...states.users import UsersState


def parse_users(users: list[User]):
    fmt = tmpl.admin.users_list_fmt
    output = []
    for u in users:
        name = user_hyperlink(u)
        output.append(fmt.format(id=u.id, name=name, user_id=u.user_id))
    return output


def split_html(text: str) -> list[str]:
    max_len = 2048

    def u16len(s: str) -> int:
        return len(s.encode("utf-16-le")) // 2

    parts, buffer = [], ""
    for line in text.splitlines(keepends=True):
        if u16len(buffer + line) > max_len:
            if buffer:
                parts.append(buffer)
            buffer = line
            if u16len(buffer) > max_len:
                while u16len(buffer) > max_len:
                    cut = buffer[:max_len]
                    parts.append(cut)
                    buffer = buffer[max_len:]
        else:
            buffer += line
    if buffer:
        parts.append(buffer)
    return parts


@router.message(AccessLevelFilter(ACCESSES["moderator"]), Command("users"))
async def users_handler(
    msg: Message, command: CommandObject, wmsg: Message, state: FSMContext
):
    total = len(await user_crud.get_all())
    await state.update_data(total_users=total)

    users = await user_crud.get_all(count=USERS_AMOUNT)
    id_range = [users[0].id, users[-1].id] if users else [1, USERS_AMOUNT]
    await state.update_data(users=users)

    prev_users = await user_crud.get_all(
        count=USERS_AMOUNT, start_id=total - USERS_AMOUNT + 1
    )
    prev_id_range = (
        [prev_users[0].id, prev_users[-1].id] if prev_users else [1, USERS_AMOUNT]
    )
    await state.update_data(prev_users=prev_users)

    next_users = await user_crud.get_all(count=USERS_AMOUNT, start_id=id_range[1] + 1)
    next_id_range = (
        [next_users[0].id, next_users[-1].id] if next_users else [1, USERS_AMOUNT]
    )
    await state.update_data(next_users=next_users)

    parsed = parse_users(users)
    text = tmpl.admin.users.format("\n".join(parsed), total)
    await wmsg.edit_text(
        text, reply_markup=kb(USERS_AMOUNT, total, prev_id_range, next_id_range)
    )
    await state.set_state(UsersState.search)


@router.callback_query(
    AccessLevelFilter(ACCESSES["moderator"]), F.data.startswith("users:move")
)
async def users_move_callback(q: CallbackQuery, state: FSMContext):
    destination = q.data.split(":")[-1]

    data = await state.get_data()
    total = data.get("total_users", 0)

    prev_move_users = data.get("users", [0, 0])
    pm_id_range = (
        [prev_move_users[0].id, prev_move_users[-1].id]
        if prev_move_users
        else [1, USERS_AMOUNT]
    )

    if destination == "<":
        users = data.get("prev_users", [0, 0])
        id_range = [users[0].id, users[-1].id] if users else [1, USERS_AMOUNT]

        prev_id_range, subtracted = id_range.copy(), 0
        while prev_id_range == id_range or not prev_id_range:
            subtracted += USERS_AMOUNT
            difference = id_range[0] - subtracted
            if difference < 0:
                id_range[0], subtracted = total, 0
                difference = id_range[0] - subtracted
            prev_users = await user_crud.get_all(
                count=USERS_AMOUNT, start_id=difference
            )
            prev_id_range = (
                [prev_users[0].id, prev_users[-1].id]
                if prev_users
                else [1, USERS_AMOUNT]
            )

        ranges = {"prev_id_range": prev_id_range, "next_id_range": pm_id_range}
        await state.update_data(prev_users=prev_users, next_users=prev_move_users)

    elif destination == ">":
        users = data.get("next_users", [])
        id_range = [users[0].id, users[-1].id] if users else [1, USERS_AMOUNT]

        next_id_range, summand = id_range.copy(), -USERS_AMOUNT
        while next_id_range == id_range or not next_id_range:
            summand += USERS_AMOUNT
            sm = id_range[1] + summand + 1
            if sm > total:
                id_range[1], summand = 1, 0
                sm = id_range[1] + summand + 1
            next_users = await user_crud.get_all(count=USERS_AMOUNT, start_id=sm)
            next_id_range = (
                [next_users[0].id, next_users[-1].id]
                if next_users
                else [1, USERS_AMOUNT]
            )

        ranges = {"prev_id_range": pm_id_range, "next_id_range": next_id_range}
        await state.update_data(prev_users=prev_move_users, next_users=next_users)

    await state.update_data(users=users)
    parsed = parse_users(users)
    text = tmpl.admin.users.format("\n".join(parsed), total)
    await q.message.edit_text(text, reply_markup=kb(USERS_AMOUNT, total, **ranges))


@router.message(AccessLevelFilter(ACCESSES["moderator"]), UsersState.search)
async def search_handler(msg: Message, wmsg: Message):
    first_name = msg.text

    dbusers = await user_crud.get_all(first_name=first_name)
    parsed = parse_users(dbusers)

    text = tmpl.admin.users.format("\n".join(parsed), len(parsed))
    parts = split_html(text)
    await wmsg.edit_text(parts[0])

    for part in parts[1:]:
        await wmsg.answer(part)
