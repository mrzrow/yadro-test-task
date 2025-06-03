from datetime import datetime
from pydantic import BaseModel, HttpUrl, ConfigDict


class UrlCreateDto(BaseModel):
    url: HttpUrl


class UrlDto(BaseModel):
    id: int
    url: HttpUrl
    short_url: str
    clicks: int
    created_at: datetime
    expired_after: int

    model_config = ConfigDict(from_attributes=True)
