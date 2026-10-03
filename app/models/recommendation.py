from datetime import datetime
from datetime import timezone

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import Float

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from ..database import Base


class Recommendation(Base):

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )

    planner_type: Mapped[str] = mapped_column(
        String(30),
        index=True
    )

    budget: Mapped[float] = mapped_column(
        Float
    )

    request_data: Mapped[dict] = mapped_column(
        JSON
    )

    result_data: Mapped[dict] = mapped_column(
        JSON
    )

    source: Mapped[str] = mapped_column(
        String(30),
        default="fallback"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    user = relationship(
        "User",
        back_populates="recommendations"
    )