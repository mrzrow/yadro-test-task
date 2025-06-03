from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from src.repositories.url import UrlRepositoryBase, UrlRepository


class UnitOfWorkBase(ABC):
    url: UrlRepositoryBase

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class UnitOfWork(UnitOfWorkBase):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def __aenter__(self):
        self.url = UrlRepository(self._session)
        return self

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
