from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.unit_of_work import UnitOfWork
from .unit_of_work import get_unit_of_work
from src.services.url import UrlService


def get_url_service(
        uow: UnitOfWork = Depends(get_unit_of_work)
) -> UrlService:
    return UrlService(uow)