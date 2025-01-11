from . import tables


def add_data(data: dict):
    tables.insert(data)


def get_data(columns: list, wh_data: dict, comparison_operator: str = "="):
    d = tables.select(columns, wh_data, comparison_operator)
    if d and d[0]:
        return d[0]


def get_all_data(data: dict, comparison_operator: str = "="):
    return get_data(["*"], data, comparison_operator)
    # d = tables.select_all(data)
    # if d and d[0]:
    #     return d[0]


def is_data_in(data: dict, comparison_operator: str = "="):
    return True if get_all_data(data, comparison_operator) else False


def update_data(new_data: dict, wh_data: dict, comparison_operator: str = "="):
    tables.update(new_data, wh_data, comparison_operator)


def remove_data(data: str, wh_data: dict, comparison_operator: str = "="):
    update_data({data: None}, wh_data, comparison_operator)


def remove_from_table(wh_data: dict, comparison_operator: str = "="):
    tables.delete_value(*wh_data.items(), comparison_operator)
