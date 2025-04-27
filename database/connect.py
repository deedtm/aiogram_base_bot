import os
from config.database import DB_PATH
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from sqlalchemy.orm import declarative_base

# Ensure database file directory exists
dirpath = os.path.dirname(DB_PATH)
if (dirpath):
    os.makedirs(dirpath, exist_ok=True)

# URL for SQLite connection via aiosqlite
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
# Фабрика асинхронных сессий
async_session = async_sessionmaker(engine, expire_on_commit=False)
# Базовый класс для моделей
Base = declarative_base()

# Import models to register in metadata
from . import models

async def init_db() -> None:
    """Initialize database schema (create tables)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Asynchronous SQLAlchemy session generator"""
    async with async_session() as session:
        yield session
