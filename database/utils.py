from . import tables
from .__utils import (
    is_data_in,
    add_data,
    get_all_data,
    get_data,
    update_data,
    remove_from_table,
)
from .constants import DATETIME_FORMAT
from .log import logger
from config.database import TABLE_NAME, TABLE_COLUMNS
from config.time import TZ
from aiogram.types import User
from datetime import datetime
from html import escape


def create_tables():
    tables.create(TABLE_NAME, TABLE_COLUMNS, "IF NOT EXISTS")
    logger.debug(f"Table {TABLE_NAME} created")
    return TABLE_NAME


def is_user_in(user_id: int):
    return is_data_in({"user_id": user_id})


def add_user(user: User):
    user_data = {
        "user_id": user.id,
        "username": user.username,
        "first_name": escape(user.first_name),
        "last_name": escape(user.last_name),
        "register_date": datetime.now(TZ).strftime(DATETIME_FORMAT),
    }
    add_data(user_data)
    logger.debug(f"{user.id} added to database")


def get_user(user_id: int):
    return get_all_data({"user_id": user_id})[1:]


def get_username(user_id: int):
    return get_data(["username"], {"user_id": user_id})


def get_first_name(user_id: int):
    return get_data(["first_name"], {"user_id": user_id})


def get_last_name(user_id: int):
    return get_data(["last_name"], {"user_id": user_id})


def get_full_name(user_id: int):
    names = get_data(["first_name", "last_name"], {"user_id": user_id})
    return " ".join(filter(None, names)) if names else None


def get_register_date(user_id: int):
    date = get_data(["register_date"], {"user_id": user_id})[0]
    return datetime.strptime(date, DATETIME_FORMAT) if date else None


def update_username(user_id: int, username: str):
    update_data({"username": username}, {"user_id": user_id})
    logger.debug(f"{user_id} username updated to {username}")


def update_first_name(user_id: int, first_name: str):
    update_data({"first_name": first_name}, {"user_id": user_id})
    logger.debug(f"{user_id} first name updated to {first_name}")


def update_last_name(user_id: int, last_name: str):
    update_data({"last_name": last_name}, {"user_id": user_id})
    logger.debug(f"{user_id} last name updated to {last_name}")


def remove_user(user_id: int):
    remove_from_table({"user_id": user_id})
    logger.debug(f"{user_id} removed")
