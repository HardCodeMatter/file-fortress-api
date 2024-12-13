from enum import Enum
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
    id: str
    name: str
    size: int
    content_type: str
    storage_key: str

    expiration_date: datetime | None = None
    is_public: bool = False

    created_at: datetime
    updated_at: datetime

    downloads_count: int
    last_downloaded_at: datetime | None = None


class OrderBy(Enum):
    name: str = 'name'
    size: str = 'size'
    is_public: str = 'is_public'
    created_at: str = 'created_at'


class FileQueryParams(BaseModel):
    order_by: OrderBy = OrderBy.created_at
    descending: bool = False
