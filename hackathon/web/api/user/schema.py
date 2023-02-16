from __future__ import annotations

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    fullname: str
    username: str
    positions: list[str]
    team_id: int | None


class UserList(UserBase):
    users: list[UserBase]


class PositionBase(BaseModel):
    id: int
    name: str
