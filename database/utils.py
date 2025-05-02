from .constants import DATETIME_FORMAT
from .log import logger
from config.time import TZ
from aiogram.types import User as TgUser
from datetime import datetime
from html import escape
from .connect import init_db, get_session, Base
from .models import User as DBUser
from sqlalchemy import select, func
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
import random
import string


async def init_schemas():
    """Initialize database schema using SQLAlchemy"""
    logger.info("Initializing database schemas...")
    await init_db()

    table_names = list(Base.metadata.tables.keys())
    logger.info(f"Tables: {', '.join(table_names)}")
    return table_names


async def get_all_users(count: int, start_id: int = 0) -> list[DBUser]:
    """Return a list of `count` users starting from users with id >= `start_id`."""
    if count <= 0:
        return []
    async for session in get_session():
        stmt = select(DBUser)
        stmt = stmt.where(DBUser.id >= start_id)
        stmt = stmt.order_by(DBUser.id)
        stmt = stmt.limit(count)
        result = await session.execute(stmt)
        return result.scalars().all()
    return []


async def get_user(
    user_id: int | None = None, first_name: str | None = None
) -> DBUser | list[DBUser] | None:
    """Fetch a user by user_id or all users with a given first_name."""
    async for session in get_session():
        if first_name is not None:
            stmt = select(DBUser).where(DBUser.first_name == first_name)
            result = await session.execute(stmt)
            return result.scalars().all()
        if user_id is not None:
            stmt = select(DBUser).where(DBUser.user_id == user_id)
            return await session.scalar(stmt)
    return None


async def add_user(user: TgUser) -> DBUser:
    """Add a new user to the database or return existing"""
    # Сначала проверяем, есть ли пользователь в БД
    existing = await get_user(user.id)
    if existing:
        return existing
    # Иначе создаём нового
    async for session in get_session():
        new_user = DBUser(
            user_id=user.id,
            username=user.username,
            first_name=escape(user.first_name),
            last_name=escape(user.last_name) if user.last_name else None,
            register_date=datetime.now(TZ).strftime(DATETIME_FORMAT),
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        logger.debug(f"User {user.id} added as ORM record")
        return new_user


async def get_user_data(
    user_id: int | None = None, first_name: str | None = None
) -> dict | list[dict] | None:
    """Return all user data as a dict, a list of dicts, or None if not found"""
    users = await get_user(user_id, first_name)
    if not users:
        return None

    def to_dict(u: DBUser) -> dict:
        return {
            "id": u.id,
            "user_id": u.user_id,
            "username": u.username,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "register_date": u.register_date,
            "access_level": u.access_level,
        }

    if isinstance(users, list):
        return [to_dict(u) for u in users]

    return to_dict(users)


async def get_username(user_id: int) -> str | None:
    """Return the user's username or None"""
    user = await get_user(user_id)
    return user.username if user else None


async def get_first_name(user_id: int) -> str | None:
    """Return the user's first name or None"""
    user = await get_user(user_id)
    return user.first_name if user else None


async def get_last_name(user_id: int) -> str | None:
    """Return the user's last name or None"""
    user = await get_user(user_id)
    return user.last_name if user else None


async def get_register_date(user_id: int) -> str | None:
    """Return the user's registration date or None"""
    user = await get_user(user_id)
    return user.register_date if user else None


async def get_access_level(user_id: int) -> int | None:
    """Return the user's access level or None"""
    user = await get_user(user_id)
    return user.access_level if user else None


async def update_user_data(user_id: int, **fields) -> bool:
    """Update user fields, return True if updated, False if user not found"""
    async for session in get_session():
        result = await session.execute(
            sqlalchemy_update(DBUser).where(DBUser.user_id == user_id).values(**fields)
        )
        if result.rowcount:
            await session.commit()
            logger.debug(f"User {user_id} updated fields {list(fields.keys())}")
            return True
        return False


async def set_username(user_id: int, username: str) -> bool:
    """Set the user's username"""
    return await update_user_data(user_id, username=username)


async def set_first_name(user_id: int, first_name: str) -> bool:
    """Set the user's first name"""
    return await update_user_data(user_id, first_name=first_name)


async def set_last_name(user_id: int, last_name: str) -> bool:
    """Set the user's last name"""
    return await update_user_data(user_id, last_name=last_name)


async def set_access_level(user_id: int, access_level: int) -> bool:
    """Set the user's access level"""
    return await update_user_data(user_id, access_level=access_level)


async def delete_user(user_id: int) -> bool:
    """Delete a user by user_id, return True if deleted, False otherwise"""
    async for session in get_session():
        result = await session.execute(
            sqlalchemy_delete(DBUser).where(DBUser.user_id == user_id)
        )
        if result.rowcount:
            await session.commit()
            logger.debug(f"User {user_id} deleted")
            return True
        return False


async def add_random_users(count: int, first_name: str | None = None) -> list[DBUser]:
    """Add specified number of randomly generated users to the database."""
    users: list[DBUser] = []
    async for session in get_session():
        for _ in range(count):
            user_id = random.randint(1000000000, 9999999999)
            username = "".join(random.choices(string.ascii_lowercase, k=8))
            if not first_name:
                first_name = "".join(random.choices(string.ascii_letters, k=6))
            last_name = "".join(random.choices(string.ascii_letters, k=6))
            reg_date = datetime.now(TZ).strftime(DATETIME_FORMAT)
            new_user = DBUser(
                user_id=user_id,
                username=username,
                first_name=escape(first_name),
                last_name=escape(last_name),
                register_date=reg_date,
            )
            session.add(new_user)
            users.append(new_user)
        await session.commit()
        for u in users:
            await session.refresh(u)
        return users
    return users


async def get_last_user_id() -> int | None:
    """Return the id of the last (highest id) user in the database, or None if no users."""
    async for session in get_session():
        stmt = select(DBUser.id).order_by(DBUser.id.desc()).limit(1)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    return None
