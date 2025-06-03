from pydantic import HttpUrl

from src.db.unit_of_work import UnitOfWork
from src.models.dto.url import UrlDto, UrlCreateDto
from src.models.url import Url

from src.utils.alias import generate_alias, is_expired
from src.config.config import settings


class UrlService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get(self, offset: int = 0, limit: int = 100) -> list[UrlDto]:
        urls = await self.uow.url.list(offset=offset, limit=limit)
        return [UrlDto.model_validate(url, from_attributes=True) for url in urls]
    
    async def get_by_id(self, id: int) -> UrlDto | None:
        url = await self.uow.url.list(id=id)
        if not url:
            return None
        return UrlDto.model_validate(url[0], from_attributes=True)
    
    async def get_by_short_url(self, alias: str) -> UrlDto | None:
        url = await self.uow.url.list(short_url=alias)
        if not url:
            return None
        url = url[0]

        if is_expired(url.created_at, url.expired_after):
            return None
        
        url.clicks += 1
        await self.uow.url.update(url)
        await self.uow.commit()
        
        return UrlDto.model_validate(url, from_attributes=True)
    
    async def get_short_url(self, id: int) -> HttpUrl | None:
        url = await self.uow.url.list(id=id)
        if not url:
            return None
        
        url = url[0]
        alias = url.short_url
        return HttpUrl.build(
            scheme='http',
            host=settings.host,
            port=int(settings.port),
            path=alias
        )
    
    async def create(self, url_create: UrlCreateDto) -> UrlDto:
        url_str = str(url_create.url)
        url_alias = generate_alias()

        url = Url(url=url_str, short_url=url_alias)
        url = await self.uow.url.add(url)
        await self.uow.commit()
        return UrlDto.model_validate(url, from_attributes=True)
    
    async def delete(self, id: int) -> None:
        await self.uow.url.delete(id=id)
        await self.uow.commit()

    async def get_statistics(self) -> dict[str, int]:
        urls = await self.uow.url.list(order_by='clicks', descending=True)
        return [UrlDto.model_validate(url, from_attributes=True) for url in urls]
