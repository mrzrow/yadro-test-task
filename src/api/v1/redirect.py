from fastapi.responses import RedirectResponse
from fastapi import Depends, APIRouter, HTTPException
from src.depends.url import get_url_service
from src.services.url import UrlService


router = APIRouter(tags=['redirect'])


@router.get('/{alias}', response_class=RedirectResponse)
async def redirect_to_url(
    alias: str,
    service: UrlService = Depends(get_url_service)
) -> RedirectResponse:
    try:
        url = await service.get_by_short_url(alias)
        if not url:
            raise HTTPException(status_code=404, detail='URL not found or expired')
        return RedirectResponse(url=url.url)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred: {str(e)}'
        )