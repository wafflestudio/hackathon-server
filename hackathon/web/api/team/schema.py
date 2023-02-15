from pydantic import BaseModel

from hackathon.web.api.user.schema import UserBase


class TeamBase(BaseModel):
    id: int
    name: str
    resolution: str
    max_members: int
    members: list[UserBase]
    applicants: list[UserBase]


class TeamList(TeamBase):
    teams: list[TeamBase]
