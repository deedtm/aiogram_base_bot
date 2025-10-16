from .types.ibutton import IButton
from .__utils import build


def kb(
    users_on_page: int,
    total: int,
    prev_id_range: list[int, int] = [],
    next_id_range: list[int, int] = [],
):
    prev = prev_id_range.copy()
    if not prev:
        prev = [total - users_on_page, total]
    prev.extend(["↩️", "<"])

    next = next_id_range.copy()
    if not next:
        next = [1, users_on_page]
    next.extend(["↪️", ">"])

    ranges = (prev, next)

    buttons = []
    for r in ranges:
        if r[0] < 0:
            r = total - users_on_page, total, "↩️", "<"
        if r[0] > total:
            r = 1, users_on_page, "↪️", ">"
        button = IButton(
            text=f"{r[2]} {r[0]} - {r[1]}",
            callback_data=f"users:move:{r[3]}",
        )
        buttons.append(button)

    return build(buttons)
