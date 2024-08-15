import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .service import UserService
from .utils import verify_password
from config import settings


async def authenticate_user(session: AsyncSession, username: str, plain_password: str) -> User:
    user: User = await UserService(session).get_user_by_username(username)

    if not user or not verify_password(plain_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password.',
        )

    return user


def create_access_token(data: dict) -> str:
    to_encode: dict = data.copy()
    expire: datetime = datetime.utcnow() + timedelta(settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.AUTH_SECRET_KEY,
        algorithm=settings.AUTH_ALGORITHM,
    )

    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode: dict = data.copy
    expire: datetime = datetime.utcnow() + timedelta(days=settings.AUTH_REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.AUTH_SECRET_KEY,
        algorithm=settings.AUTH_ALGORITHM,
    )

    return encoded_jwt
