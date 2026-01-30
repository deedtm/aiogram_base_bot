from typing import Generic, TypeVar

from loguru import logger as l
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import select
from sqlalchemy import update as sqlalchemy_update

T = TypeVar("T")


class CRUDBase(Generic[T]):
    model = None

    def __init__(self, session_getter):
        self.get_session = session_getter

    async def get_all(self, *where, count=0, start_id=0, **filters) -> list[T]:
        async for session in self.get_session():
            stmt = select(self.model).where(self.model.id >= start_id)
            for expr in where:
                stmt = stmt.where(expr)
            for k, v in filters.items():
                stmt = stmt.where(getattr(self.model, k) == v)
            stmt = stmt.order_by(self.model.id)
            if count > 0:
                stmt = stmt.limit(count)
            result = await session.execute(stmt)
            return result.scalars().all()
        return []

    async def get_one(self, *where, **filters) -> T | None:
        async for session in self.get_session():
            stmt = select(self.model)
            for expr in where:
                stmt = stmt.where(expr)
            for k, v in filters.items():
                stmt = stmt.where(getattr(self.model, k) == v)
            return await session.scalar(stmt)
        return None

    async def add(self, obj: T = None, **fields) -> T:
        async for session in self.get_session():
            if obj is not None:
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                l.debug(
                    f"{self.model.__name__} added (object): {', '.join(f'{k}={v}' for k, v in obj.as_dict.items())}"
                )
                return obj
            else:
                obj = self.model(**fields)
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                l.debug(
                    f"{self.model.__name__} added: {', '.join(f'{k}={v}' for k, v in obj.as_dict.items())}"
                )
                return obj

    async def update(self, id_field, id_value, **fields) -> bool:
        async for session in self.get_session():
            result = await session.execute(
                sqlalchemy_update(self.model)
                .where(getattr(self.model, id_field) == id_value)
                .values(**fields)
            )
            if result.rowcount:
                l.debug(
                    f"{self.model.__name__} {id_field}={id_value} updated fields {list(fields.keys())}"
                )
                await session.commit()
                return True
            return False

    async def delete(self, id_field, id_value) -> bool:
        async for session in self.get_session():
            result = await session.execute(
                sqlalchemy_delete(self.model).where(
                    getattr(self.model, id_field) == id_value
                )
            )
            if result.rowcount:
                l.debug(f"{self.model.__name__} {id_field}={id_value} deleted")
                await session.commit()
                return True
            return False
