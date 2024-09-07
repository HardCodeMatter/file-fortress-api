from fastapi import HTTPException, status
from sqlalchemy import select, Select

from .models import User
from .schemas import UserCreate, ChangeUserPassword
from .utils import hash_password, verify_password
from service import BaseService


class UserService(BaseService):
    async def create_user(self, user_data: UserCreate) -> User:
        stmt: Select[User] = select(User).filter((User.username == user_data.username) | (User.email == user_data.email))
        user: User = (
            await self.session.execute(stmt)
        ).scalars().first()

        if user:
            if user.username == user_data.username:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f'User with this username is already exist.'
                )

            if user.email == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f'User with this email is already exist.'
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

    async def change_user_password(self, username: str, password_data: ChangeUserPassword) -> dict[str, str]:
        stmt = select(User).filter(User.username == username)
        user: User = (await self.session.execute(stmt)).scalar()

        if not verify_password(password_data.old_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Old password is incorrect.',
            )

        hashed_password = hash_password(password_data.new_password)
        user.hashed_password = hashed_password

        self.session.add(user)
        await self.session.commit()

        return {
            'detail': 'Password changed successfully.'
        }
