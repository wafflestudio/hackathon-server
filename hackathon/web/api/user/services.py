from fastapi import Depends, HTTPException

from hackathon.web.api.user.repositories import UserRepository

from .schema import PositionBase, UserBase


class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    async def get_user_by_id(self, id: int) -> UserBase:
        user = await self.user_repository.get_user_by_id(id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user.to_pydantic()

    async def get_users(self) -> list[UserBase]:
        users = await self.user_repository.get_users()
        return [user.to_pydantic() for user in users]

    async def get_positions(self) -> list[PositionBase]:
        positions = await self.user_repository.get_positions()
        return [
            PositionBase(
                id=position.id,
                name=position.name,
            )
            for position in positions
        ]
