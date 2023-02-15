from pydantic import BaseModel

from hackathon.web.api.user.schema import UserBase


class TeamBase(BaseModel):
    id: int
    name: str
    resolution: str
    maxMembers: int
    members: list[UserBase]
    applicants: list[UserBase]


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
