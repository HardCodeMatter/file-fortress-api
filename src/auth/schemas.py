from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(UserBase):
    hashed_password: str


class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
