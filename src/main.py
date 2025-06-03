from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from fastapi import Depends, FastAPI, HTTPException

from .api import router_v1, redirect_router
from .models.base import Base
from .db.session import engine
from .config.config import settings
from .services.url import UrlService
from .depends.url import get_url_service


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(
    title='Yadro Test Task',
    lifespan=lifespan,
)
app.include_router(router_v1, prefix=settings.prefix)
app.include_router(redirect_router)
