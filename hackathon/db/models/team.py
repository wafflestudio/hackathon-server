from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hackathon.db.base import Base

if TYPE_CHECKING:
    from hackathon.db.models.user import User
    from hackathon.web.api.team.schema import TeamBase


class Team(Base):
    """Team model."""

    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432
    resolution: Mapped[str] = mapped_column(Text)
    max_members: Mapped[int]

    members: Mapped[list[User]] = relationship(back_populates="team")
    applicants: Mapped[list[User]] = relationship(back_populates="team")

    def to_pydantic(self) -> TeamBase:
        """Convert SQLAlchemy model to Pydantic model."""
        from hackathon.web.api.team.schema import TeamBase

        return TeamBase(
            id=self.id,
            name=self.name,
            resolution=self.resolution,
            max_members=self.max_members,
            members=[member.to_pydantic() for member in self.members],
            applicants=[applicant.to_pydantic() for applicant in self.applicants],
        )
