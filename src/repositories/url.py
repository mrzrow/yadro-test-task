from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.url import Url
from .abstract import GenericRepository, GenericSqlRepository


class UrlRepositoryBase(GenericRepository[Url], ABC):
    pass


class UrlRepository(GenericSqlRepository[Url], UrlRepositoryBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Url)
