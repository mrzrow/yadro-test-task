from pydantic import HttpUrl
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException

from src.depends import get_url_service
from src.models.dto.url import UrlDto, UrlCreateDto
from src.services.url import UrlService


router = APIRouter(prefix='/url', tags=['url'])


@router.get('/', response_model=list[UrlDto])
async def get_urls(
    offset: int = 0,
    limit: int = 100,
    service: UrlService = Depends(get_url_service)
) -> list[UrlDto]:
    return await service.get(offset=offset, limit=limit)


@router.post('/', response_model=UrlDto)
async def create_url(
    url_create: UrlCreateDto,
    service: UrlService = Depends(get_url_service)
) -> UrlDto:
    try:
        return await service.create(url_create=url_create)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail='Failed to create a short URL, please try again'
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred: {str(e)}'
        )
    

@router.get('/statistics', response_model=list[UrlDto])
async def get_statistics(
    service: UrlService = Depends(get_url_service)
) -> list[UrlDto]:
    try:
        return await service.get_statistics()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred: {str(e)}'
        )


@router.get('/{id}', response_model=UrlDto)
async def get_url_by_id(
    id: int,
    service: UrlService = Depends(get_url_service)
) -> UrlDto:
    try:
        url = await service.get_by_id(id)
        if not url:
            raise HTTPException(status_code=404, detail='URL not found')
        return url
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred: {str(e)}'
        )


@router.get('/{id}/short', response_model=HttpUrl)
async def get_short_url(
    id: int,
    service: UrlService = Depends(get_url_service)
) -> HttpUrl:
    try:
        short_url = await service.get_short_url(id)
        if short_url is None:
            raise HTTPException(status_code=404, detail='URL not found')
        return short_url
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred: {str(e)}'
        )

    
@router.delete('/{id}', status_code=204)
async def delete_url(
    id: int,
    service: UrlService = Depends(get_url_service)
) -> None:
    try:
        await service.delete(id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred: {str(e)}'
        )
