from fastapi import APIRouter
from .v1.url import router as url_router
from .v1.redirect import router as redirect_router


router_v1 = APIRouter()
router_v1.include_router(url_router)

__all__ = (
    'router_v1',
    'redirect_router',
)
