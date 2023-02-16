from pydantic import BaseModel


class SignUpRequest(BaseModel):
    fullname: str
    username: str
    password: str
    positions: list[str]


class SignInRequest(BaseModel):
    username: str
    password: str


class SignInResponse(BaseModel):
    class UserAttributes(BaseModel):
        id: int
        fullname: str
        username: str
        position: list[str]
        team_id: int | None

    token: str
    user: UserAttributes
