import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models import IDMixin, TimestampMixin

if typing.TYPE_CHECKING:
    from files.models import File


class User(IDMixin, TimestampMixin, Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    first_name: Mapped[str]
    last_name: Mapped[str]

    hashed_password: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    files: Mapped[list['File']] = relationship(back_populates='uploader')

    def __str__(self) -> str:
        return f'User(id={self.id}, username={self.username}, is_superuser={self.is_superuser})'

    def __repr__(self) -> str:
        return self.__str__
