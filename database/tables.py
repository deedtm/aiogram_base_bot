from .__tables_utils import format_values, get_table
from .connect import cursor
from .constants import QUERIES


queries = QUERIES["tables"]


def create(name: str, columns: list, condition: str = ""):
    f_cols = ",\n".join(columns)
    query = "create"
    kwargs = {"name": name, "columns": f_cols, "condition": condition + " "}

    query_wrapper(query, **kwargs)


def delete(name: str):
    query = "delete"
    kwargs = {"name": name}
    query_wrapper(query, **kwargs)


def delete_value(column: str, value: str, comparison_operator: str = "="):
    query = "delete_value"
    kwargs = {"column": column, "comp_op": comparison_operator, "value": value}
    query_wrapper(query, **kwargs)


def insert(columns: dict[str]):
    cols = ", ".join(columns.keys())
    vals = format_values(columns)

    query = "insert"
    kwargs = {"columns": cols, "values": vals}
    query_wrapper(query, **kwargs)


def update(
    columns: dict,
    wh_columns: dict[str] = None,
    comparison_operator: str = "=",
):
    column = "".join(columns.keys())
    value = format_values(columns)

    query = "update"
    kwargs = {"column": column, "value": value}

    if wh_columns is None:
        query_wrapper(query, **kwargs)
        return

    kwargs.setdefault("comp_op", comparison_operator)
    wh_qwrapper(query, wh_columns, **kwargs)


def select(
    columns: list[str],
    wh_columns: dict[str] = None,
    comparison_operator: str = "=",
):
    query = "select"
    kwargs = {"columns": ", ".join(columns)}

    if wh_columns is None:
        return query_wrapper(query, **kwargs)

    kwargs.setdefault("comp_op", comparison_operator)
    return wh_qwrapper(query, wh_columns, **kwargs)


def select_all(
    wh_columns: dict[str] = None,
    comparison_operator: str = "=",
):
    kwargs = {"columns": "*"}

    if wh_columns is None:
        return query_wrapper("select", **kwargs)

    kwargs.setdefault("comp_op", comparison_operator)
    return wh_qwrapper("select", wh_columns, **kwargs)


def query_wrapper(query: str, **kwargs):
    template = queries[query]
    operation = template.format(table=get_table(), **kwargs)
    cursor.execute(operation)

    try:
        return cursor.fetchall()
    except TypeError:
        return


def wh_qwrapper(query: str, wh_columns: dict, **kwargs):
    query += "_wh"
    wh_name = "".join(wh_columns.keys())
    wh_value = format_values(wh_columns)

    return query_wrapper(query, wh_columns=wh_name, wh_value=wh_value, **kwargs)
