import itertools

from aiogram import F
from aiogram.types import Message, CallbackQuery, MessageEntity
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext

from config.telegram import USERS_LIST_AMOUNT as USERS_AMOUNT
from database.utils import get_all_users, add_random_users, get_last_user_id, get_user
from database.models import User
from templates.enums.commands import Commands as tmpl
from templates.enums.exceptions import Exceptions as tmpl_ex

from ...filters.access_level import AccessLevelFilter
from ...objects import router
from ...utils import get_user_hyperlink
from ...keyboards.inline.users import kb
from ...states.users import UsersState


def parse_users(users: list[User]):
    fmt = tmpl.admin.users_list_fmt
    output = []
    for u in users:
        name = get_user_hyperlink(u)
        output.append(fmt.format(id=u.id, name=name, user_id=u.user_id))
    return output


def split_html(text: str) -> list[str]:
    max_len = 2048
    
    def u16len(s: str) -> int:
        return len(s.encode('utf-16-le')) // 2
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


@router.message(AccessLevelFilter(2), Command("users"))
async def users_handler(
    msg: Message, command: CommandObject, wmsg: Message, state: FSMContext
):
    total = await get_last_user_id()
    await state.update_data(total_users=total)

    users = await get_all_users(USERS_AMOUNT)
    id_range = [users[0].id, users[-1].id] if users else [1, USERS_AMOUNT]
    await state.update_data(users=users)

    prev_users = await get_all_users(USERS_AMOUNT, total - USERS_AMOUNT + 1)
    prev_id_range = (
        [prev_users[0].id, prev_users[-1].id] if prev_users else [1, USERS_AMOUNT]
    )
    await state.update_data(prev_users=prev_users)

    next_users = await get_all_users(USERS_AMOUNT, id_range[1] + 1)
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


@router.callback_query(AccessLevelFilter(2), F.data.startswith("users:move"))
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
            prev_users = await get_all_users(USERS_AMOUNT, difference)
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
            next_users = await get_all_users(USERS_AMOUNT, sm)
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


@router.message(AccessLevelFilter(2), UsersState.search)
async def search_handler(msg: Message, wmsg: Message):
    first_name = msg.text

    dbusers = await get_user(first_name=first_name)
    parsed = parse_users(dbusers)

    text = tmpl.admin.users.format("\n".join(parsed), len(parsed))
    parts = split_html(text)
    await wmsg.edit_text(parts[0])
        
    for part in parts[1:]:
        await wmsg.answer(part)


@router.message(AccessLevelFilter(3), Command("random_users"))
async def random_users_handler(msg: Message, command: CommandObject, wmsg: Message):
    if not command.args:
        await wmsg.edit_text(tmpl_ex.no_args)
        return
    args = command.args.split()
    amount = int(args[0])
    if len(args) == 2:
        first_name = args[1]
    await add_random_users(amount, first_name)
    text = tmpl.admin.random_users.format(amount)
    await wmsg.edit_text(text)
