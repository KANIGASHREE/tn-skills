from datetime import datetime
from datetime import timezone

from sqlalchemy import DateTime
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    full_name: Mapped[str] = mapped_column(
        String(120)
    )

    password_hash: Mapped[str] = mapped_column(
        String(255)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="user",
        cascade="all, delete-orphan"
    )