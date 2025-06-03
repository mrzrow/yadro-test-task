from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Type
from pydantic import BaseModel
from sqlalchemy.sql import Select
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T", bound=BaseModel)


class GenericRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        raise NotImplementedError()

    @abstractmethod
    async def list(
        self, 
        offset: int = 0, 
        limit: int = 100,
        order_by: Optional[str] = None,
        descending: bool = False,
        **filters
    ) -> list[T]:
        raise NotImplementedError()

    @abstractmethod
    async def add(self, record: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, record: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError()


class GenericSqlRepository(GenericRepository[T], ABC):

    def __init__(self, session: AsyncSession, model_cls: Type[T]) -> None:
        self._session = session
        self._model_cls = model_cls

    def _construct_get_stmt(self, id: int) -> Select:
        stmt = select(self._model_cls).where(self._model_cls.id == id)
        return stmt

    async def get_by_id(self, id: int) -> Optional[T]:
        stmt = self._construct_get_stmt(id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    def _construct_list_stmt(self, order_by: Optional[str] = None, descending: bool = False, **filters) -> Select:
        stmt = select(self._model_cls)
        where_clauses = []
        for c, v in filters.items():
            print(f"Filtering by {c} = {v}")
            if not hasattr(self._model_cls, c):
                raise ValueError(f"Invalid column name {c}")
            where_clauses.append(getattr(self._model_cls, c) == v)

        if where_clauses:
            stmt = stmt.where(and_(*where_clauses))
        
        print(f'Ordering by: {order_by}, descending: {descending}')
        if order_by:
            if not hasattr(self._model_cls, order_by):
                raise ValueError(f'Invalid order_by column name: {order_by}')
            column = getattr(self._model_cls, order_by)
            stmt = stmt.order_by(column.desc() if descending else column.asc())

        return stmt

    async def list(
            self,
            offset: int = 0,
            limit: int = 100,
            order_by: Optional[str] = None,
            descending: bool = False,
            **filters
        ) -> list[T]:
        stmt = self._construct_list_stmt(
            order_by=order_by,
            descending=descending,
            **filters
        )

        stmt = stmt.offset(offset).limit(limit)
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def add(self, record: T) -> T:
        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        return record

    async def update(self, record: T) -> T:
        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        return record

    async def delete(self, id: int) -> None:
        record = await self.get_by_id(id)
        if record is not None:
            await self._session.delete(record)
            await self._session.flush()
