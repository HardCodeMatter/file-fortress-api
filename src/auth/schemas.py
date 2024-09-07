import re
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationInfo, field_validator


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        if ' ' in value.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username cannot contain spaces.',
            )

        if len(value.strip()) < 2 or len(value.strip()) > 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username must be between 2 and 20 characters in length, inclusive.',
            )

        if not re.match(r'^[\w.]+$', value.strip()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username must only contain letters, numbers, underscores, and points',
            )

        return value.strip().lower()

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str) -> str:
        validation_expression = r'^[a-zA-Z0-9]+[.\w]*@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'

        if ' ' in value.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email cannot contain spaces.',
            )

        if not re.match(validation_expression, value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid email address',
            )

        return value.strip().lower()

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_first_name(cls, value: str) -> str:
        if len(value.strip()) < 2 or len(value.strip()) > 30:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Name must be between 2 and 30 characters in length, inclusive.',
            )

        if not re.match(r'^[A-Za-z]+$', value.strip()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Name must only contain letters.',
            )

        return value.strip().capitalize()


class UserCreate(UserBase):
    hashed_password: str

    @field_validator('hashed_password')
    @classmethod
    def validate_hashed_password(cls, value: str) -> str:
        pattern: str = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

        if ' ' in value.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password cannot contain spaces.',
            )

        if len(value.strip()) < 8 or len(value.strip()) > 32:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password must be between 8 and 32 characters in length, inclusive.',
            )

        if not re.match(pattern, value.strip()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password must contain at least one uppercase letter, one lowercase letter, and one number.',
            )

        return value.strip()


class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime


class ChangeUserPassword(BaseModel):
    old_password: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, value: str, info: ValidationInfo) -> str:
        pattern: str = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

        if ' ' in value.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password cannot contain spaces.',
            )

        if len(value.strip()) < 8 or len(value.strip()) > 32:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password must be between 8 and 32 characters in length, inclusive.',
            )

        if not re.match(pattern, value.strip()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password must contain at least one uppercase letter, one lowercase letter, and one number.',
            )

        if 'old_password' in info.data and value == info.data['old_password']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='New password must be different from the old password.',
            )

        return value.strip()
