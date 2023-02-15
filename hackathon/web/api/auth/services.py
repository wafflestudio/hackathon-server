from typing import TYPE_CHECKING

import bcrypt
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from hackathon.web.api.auth.repositories import AuthRepository
from hackathon.web.api.auth.schema import *

if TYPE_CHECKING:
    from hackathon.web.api.user.schema import UserBase


class AuthService:
    """Service class for authentication related operations."""

    def __init__(self, auth_repository: AuthRepository = Depends()):
        self.auth_repository = auth_repository

    async def sign_up(self, data: SignUpRequest) -> SignInResponse:
        try:
            await self.auth_repository.add_user(**data.dict())
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Username already exists")

        user = await self.auth_repository.get_user_by_username(data.username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        return SignInResponse(
            token=user.token,
            user=SignInResponse.UserAttributes(
                fullname=user.fullname,
                username=user.username,
                position=[position.name for position in user.positions],
                team_id=user.team_id,
            ),
        )

    async def sign_in(self, data: SignInRequest) -> SignInResponse:
        user = await self.auth_repository.get_user_by_username(data.username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username.")

        if bcrypt.checkpw(
            data.password.encode("utf-8"),
            user.hashed_password.encode("utf-8"),
        ):
            return SignInResponse(
                token=user.token,
                user=SignInResponse.UserAttributes(
                    fullname=user.fullname,
                    username=user.username,
                    position=[position.name for position in user.positions],
                    team_id=user.team_id,
                ),
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")

    async def get_current_user(self, token: str) -> "UserBase":
        user = await self.auth_repository.get_user_by_token(token)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
            )
        return user.to_pydantic()
