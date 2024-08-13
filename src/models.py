import uuid
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import declarative_mixin, Mapped, mapped_column


@declarative_mixin
class IDMixin:
    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=str(uuid.uuid4()))


@declarative_mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
