from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hackathon.db.base import Base

if TYPE_CHECKING:
    from hackathon.db.models.user import User


class Team(Base):
    """Team model."""

    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432
    resolution: Mapped[str] = mapped_column(Text)
    max_members: Mapped[int]

    members: Mapped[list[User]] = relationship(back_populates="team")
