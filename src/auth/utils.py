import jwt
from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from .models import User
from .schemas import TokenData
from . import service
from database import get_async_session
from config import settings


password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


async def get_current_user(
    request: Request = Request,
    session: AsyncSession = Depends(get_async_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials.',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    access_token = request.cookies.get('access_token')

    try:
        payload = jwt.decode(
            access_token,
            verify=True,
            key=settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM],
        )

        username = payload.get('sub')

        if not username:
            raise credentials_exception

        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized.',
        )

    user: User = await service.UserService(session).get_user_by_username(token_data.username)

    if not user:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User is not active.',
        )

    return current_user
