from sqlalchemy import Boolean, Text, ForeignKey, String, false, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

class ProjectPlace(Base):
    __tablename__ = "project_places"

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("travel_projects.id", ondelete="CASCADE"),
        index=True
    )

    external_id: Mapped[str] = mapped_column(String(255), nullable=False)

    notes: Mapped[str | None] = mapped_column(Text)

    visited: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false()
    )

    project: Mapped["TravelProject"] = relationship(
        back_populates="places"
    )

    __table_args__ = (
        UniqueConstraint("project_id", "external_id", name="uq_project_place"),
    )