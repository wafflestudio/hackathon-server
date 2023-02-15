from __future__ import annotations

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    fullname: str
    username: str
    positions: list[str]
    team_id: int | None
    applications: list[TeamApplicationBase]


class UserList(UserBase):
    users: list[UserBase]


from hackathon.web.api.team.schema import TeamApplicationBase

UserBase.update_forward_refs()
