from datetime import datetime
from html import escape

from aiogram.types import User as TgUser
from loguru import logger
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import func, select
from sqlalchemy import update as sqlalchemy_update

from config import TZ

from .connect import Base, get_session, init_db
from .models import User as DBUser


async def init_schemas():
    """Initialize database schema using SQLAlchemy"""
    logger.info("Initializing database schemas...")
    await init_db()

    table_names = list(Base.metadata.tables.keys())
    logger.info(f"Tables: {', '.join(table_names)}")
    return table_names


async def get_users(
    count: int = 0,
    start_id: int = 0,
    min_access_level: int | None = None,
    max_access_level: int | None = None,
) -> list[DBUser]:
    """
    Return a list of `count` users starting from users with id >= `start_id`.
    Optionally filter by minimum and/or maximum access_level.
    """
    async for session in get_session():
        stmt = select(DBUser).where(DBUser.id >= start_id)
        if min_access_level is not None:
            stmt = stmt.where(DBUser.access_level >= min_access_level)
        if max_access_level is not None:
            stmt = stmt.where(DBUser.access_level <= max_access_level)
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


async def add_user(user: TgUser, access_level: int = 1) -> DBUser:
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
            register_date=int(datetime.now(TZ).timestamp()),
            access_level=access_level,
            nickname=user.full_name,
            anonymous=True,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        logger.debug(
            f"User {user.id} added: {', '.join(f'{k}={v}' for k, v in new_user.as_dict.items())}"
        )
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


async def get_last_user_id() -> int | None:
    """Return the id of the last (highest id) user in the database, or None if no users."""
    async for session in get_session():
        stmt = select(DBUser.id).order_by(DBUser.id.desc()).limit(1)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    return None
