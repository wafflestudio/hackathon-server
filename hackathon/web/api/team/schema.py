from __future__ import annotations

from pydantic import BaseModel


class TeamBase(BaseModel):
    id: int
    name: str
    resolution: str
    maxMembers: int
    members: list[UserBase]
    applications: list[TeamApplicationBase]


class TeamList(TeamBase):
    teams: list[TeamBase]


class TeamCreate(BaseModel):
    name: str
    resolution: str
    maxMembers: int
    members: list[int] | None


class TeamApplyRequest(BaseModel):
    comment: str


class TeamOperationResult(BaseModel):
    success: bool


class TeamApplicationBase(BaseModel):
    id: int
    comment: str
    user: UserBase
    team: TeamBase


from hackathon.web.api.user.schema import UserBase

TeamBase.update_forward_refs()
TeamApplicationBase.update_forward_refs()
