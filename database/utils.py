import random
import string
from datetime import datetime
from html import escape

from aiogram.types import User as TgUser
from loguru import logger
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import func, select
from sqlalchemy import update as sqlalchemy_update

from config import TZ

from .config import DATETIME_FORMAT
from .connect import Base, get_session, init_db
from .models import User as DBUser


async def init_schemas():
    """Initialize database schema using SQLAlchemy"""
    logger.info("Initializing database schemas...")
    await init_db()

    table_names = list(Base.metadata.tables.keys())
    logger.info(f"Tables: {', '.join(table_names)}")
    return table_names


async def get_users(count: int = 0, start_id: int = 0) -> list[DBUser]:
    """Return a list of `count` users starting from users with id >= `start_id`."""
    async for session in get_session():
        stmt = select(DBUser)
        stmt = stmt.where(DBUser.id >= start_id)
        stmt = stmt.order_by(DBUser.id)
        if count > 0:
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
    existing = await get_user(user.id)
    if existing:
        return existing

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
