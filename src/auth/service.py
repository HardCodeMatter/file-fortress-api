from fastapi import HTTPException, status
from sqlalchemy import select, Select

from .models import User
from .schemas import UserCreate
from .utils import hash_password
from service import BaseService


class UserService(BaseService):
    async def create_user(self, user_data: UserCreate) -> User:
        stmt: Select[User] = select(User).filter(User.username == user_data.username)
        user: User = await self.session.execute(stmt)

        if user.username or user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'User with this {"username" if user.username else "email"} is already exist.'
            )

        user_data.hashed_password = hash_password(user_data.hashed_password)
        user = User(**user_data.model_dump())

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_user_by_username(self, username: str) -> User:
        stmt = select(User).filter(User.username == username)

        user: User = (await self.session.execute(stmt)).scalar()

        await self.session.commit()

        return user
