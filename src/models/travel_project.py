from datetime import date
from sqlalchemy import String, Date, Boolean, Text, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class TravelProject(Base):
    __tablename__ = "travel_projects"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str | None] = mapped_column(Text)

    start_date: Mapped[date | None] = mapped_column(Date)

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false()
    )

    places: Mapped[list["ProjectPlace"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )