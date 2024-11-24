import typing
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models import IDMixin, TimestampMixin

if typing.TYPE_CHECKING:
    from auth.models import User


class File(IDMixin, TimestampMixin, Base):
    __tablename__ = 'files'

    name: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)
    content_type: Mapped[str] = mapped_column(nullable=False)
    storage_key: Mapped[str] = mapped_column(index=True, nullable=False)

    uploader_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    uploader: Mapped['User'] = relationship(back_populates='files')

    access_code: Mapped[str] = mapped_column(nullable=True)
    expiration_date: Mapped[datetime] = mapped_column(nullable=True)
    is_public: Mapped[bool] = mapped_column(default=False)

    downloads_count: Mapped[int] = mapped_column(default=0)
    last_downloaded_at: Mapped[datetime] = mapped_column(nullable=True)

    def __str__(self) -> str:
        return f'File(id={self.id}, name={self.name}, size={self.size}, uploader={self.uploader}, content_type={self.content_type})'

    def __repr__(self) -> str:
        return self.__str__
