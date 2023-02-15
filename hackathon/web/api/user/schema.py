from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    fullname: str
    username: str
    positions: list[str]
    team_id: int | None


class UserList(UserBase):
    users: list[UserBase]
