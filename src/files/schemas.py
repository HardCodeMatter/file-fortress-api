import json
from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator


class FileBase(BaseModel): ...


class FileCreate(FileBase):
    access_code: str | None = None
    expiration_date: datetime | None = None
    is_public: bool = False

    model_config = ConfigDict(
        from_attributes=True,
    )


class FileRead(FileBase):
    name: str
    size: int
    content_type: str
    storage_key: str

    expiration_date: datetime | None = None
    is_public: bool = False

    downloads_count: int
    last_downloaded_at: datetime | None = None
