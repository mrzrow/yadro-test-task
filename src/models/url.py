from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from .base import Base
from src.config.config import settings


class Url(Base):
    url: Mapped[str] = mapped_column(nullable=False)
    short_url: Mapped[str] = mapped_column(nullable=False, unique=True)
    clicks: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    expired_after: Mapped[int] = mapped_column(nullable=False, default=settings.url.expiration_time)
