from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String

from hackathon.db.base import Base

if TYPE_CHECKING:
    from hackathon.web.api.user.schema import UserBase

from hackathon.db.models.team import Team

users_positions = Table(
    "users_positions",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("position_id", ForeignKey("position.id"), primary_key=True),
)


class Position(Base):
    """Position model."""

    __tablename__ = "position"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=10), unique=True)  # noqa: WPS432

    users: Mapped[list[User]] = relationship(
        secondary=users_positions,
        back_populates="positions",
    )


class User(Base):
    """User model."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(
        String(length=50),
        unique=True,
    )  # noqa: WPS432
    fullname: Mapped[str] = mapped_column(String(length=20))  # noqa: WPS432
    hashed_password: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432

    token: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432

    team_id: Mapped[int | None] = mapped_column(ForeignKey("team.id"))
    team: Mapped[Team | None] = relationship(back_populates="members")

    positions: Mapped[list[Position]] = relationship(
        secondary=users_positions,
        back_populates="users",
    )

    def to_pydantic(self) -> UserBase:
        """Convert SQLAlchemy model to Pydantic model."""
        from hackathon.web.api.user.schema import UserBase

        return UserBase(
            id=self.id,
            username=self.username,
            fullname=self.fullname,
            team_id=self.team_id,
            positions=[position.name for position in self.positions],
        )
