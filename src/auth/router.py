import jwt
from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .manager import authenticate_user, create_access_token, create_refresh_token, decode_refresh_token
from .models import User
from .schemas import Token, UserCreate, UserRead, ChangeUserPassword
from . import service
from .utils import get_current_active_user, get_current_user
from config import settings
from database import get_async_session

router: APIRouter = APIRouter(
    tags=['Authentication'],
)


@router.post('/auth/login')
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    response: Response = Response(),
    session: AsyncSession = Depends(get_async_session),
) -> Token:
    user: User = await authenticate_user(session=session, username=form_data.username, plain_password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password.'
        )

    access_token = create_access_token({'sub': user.username})
    refresh_token = create_refresh_token({'sub': user.username})

    response.set_cookie(key='access_token', value=access_token, httponly=True, max_age=settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, max_age=settings.AUTH_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer',
    )


@router.post('/auth/register', status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
) -> UserRead:
    return await service.UserService(session).create_user(user_data)


@router.post('/auth/change-password', status_code=status.HTTP_200_OK)
async def change_password(
    password_data: ChangeUserPassword,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> dict[str, str]:
    return await service.UserService(session).change_user_password(current_user.username, password_data)


@router.post('/auth/refresh', status_code=status.HTTP_200_OK)
async def refresh_tokens(
    request: Request = Request,
    response: Response = Response(),
) -> Token:
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token is not provided.'
        )

    try:
        payload = decode_refresh_token(refresh_token)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token is invalid.',
        )

    access_token = create_access_token({'sub': payload['sub']})
    refresh_token = create_refresh_token({'sub': payload['sub']})

    response.set_cookie(key='access_token', value=access_token, httponly=True, max_age=settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, max_age=settings.AUTH_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer',
    )


@router.post('/auth/logout', status_code=status.HTTP_200_OK)
async def logout(response: Response = Response()) -> dict:
    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')

    return {
        'detail': 'Logout successful.'
    }


@router.get('/users', status_code=status.HTTP_200_OK)
async def get_user_by_username(
    username: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user),
) -> UserRead:
    user: User = await service.UserService(session).get_user_by_username(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.',
        )

    return user
