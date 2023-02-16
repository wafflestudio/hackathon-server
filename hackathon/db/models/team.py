from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hackathon.db.base import Base

if TYPE_CHECKING:
    from hackathon.db.models.user import User
    from hackathon.web.api.team.schema import TeamApplicationBase, TeamBase


class Team(Base):
    """Team model."""

    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432
    resolution: Mapped[str] = mapped_column(Text)
    max_members: Mapped[int]

    members: Mapped[list[User]] = relationship(back_populates="team")

    team_applications: Mapped[list[TeamApplication]] = relationship(
        back_populates="team",
        cascade="all, delete",
    )

    def to_pydantic(self) -> TeamBase:
        """Convert SQLAlchemy model to Pydantic model."""
        from hackathon.web.api.team.schema import TeamBase

        return TeamBase(
            id=self.id,
            name=self.name,
            resolution=self.resolution,
            maxMembers=self.max_members,
            members=[member.id for member in self.members],
            applications=[
                application.to_pydantic() for application in self.team_applications
            ],
        )


class TeamApplication(Base):
    """Team application model."""

    __tablename__ = "team_application"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    comment: Mapped[str] = mapped_column(Text)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="team_applications")

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    team: Mapped[Team] = relationship(back_populates="team_applications")

    __table_args__ = (UniqueConstraint("user_id", "team_id"),)

    def to_pydantic(self) -> TeamApplicationBase:
        """Convert SQLAlchemy model to Pydantic model."""
        from hackathon.web.api.team.schema import TeamApplicationBase

        return TeamApplicationBase(
            id=self.id,
            comment=self.comment,
            user_id=self.user_id,
            team_id=self.team_id,
        )
