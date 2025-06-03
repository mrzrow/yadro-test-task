import os

from datetime import datetime
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv


load_dotenv(Path(__file__).parent.parent.parent / '.env')


class DBSettings(BaseModel):
    url: str = os.environ.get('DB_URL')
    echo: bool = os.environ.get('DB_ECHO', 'false').lower() == 'true'


class UrlSettings(BaseModel):
    expiration_time: int = int(os.environ.get('URL_EXPIRATION_TIME', '3600'))
    alias_length: int = int(os.environ.get('ALIAS_LENGTH', '10'))


class Settings(BaseModel):
    db: DBSettings = DBSettings()
    url: UrlSettings = UrlSettings()
    prefix: str = os.environ.get('API_PREFIX')
    

settings = Settings()
