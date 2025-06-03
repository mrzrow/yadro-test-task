from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.config.config import settings


engine = create_async_engine(
    url=settings.db.url,
    echo=settings.db.echo,
    future=True,
)

Session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session
