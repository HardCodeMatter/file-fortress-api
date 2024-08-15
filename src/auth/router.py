from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .manager import authenticate_user, create_access_token, create_refresh_token
from .models import User
from .schemas import Token, UserCreate, UserRead
from . import service
from database import get_async_session


router: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Authentication'],
)


@router.post('/login')
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
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

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer',
    )


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
) -> UserRead:
    return await service.UserService(session).create_user(user_data)
