from __future__ import annotations

from pydantic import BaseModel


class TeamBase(BaseModel):
    id: int
    name: str
    resolution: str
    maxMembers: int
    members: list[int]


class TeamDetail(TeamBase):
    members: list[UserBase]
    applications: list[TeamApplicationBase]


class TeamList(TeamBase):
    teams: list[TeamBase]


class TeamCreateRequest(BaseModel):
    name: str
    resolution: str
    maxMembers: int


class TeamApplyRequest(BaseModel):
    comment: str


class TeamOperationResult(BaseModel):
    success: bool


class TeamApplicationBase(BaseModel):
    id: int
    comment: str
    user: UserBase
    team_id: int


from hackathon.web.api.user.schema import UserBase

TeamBase.update_forward_refs()
TeamApplicationBase.update_forward_refs()
TeamDetail.update_forward_refs()
