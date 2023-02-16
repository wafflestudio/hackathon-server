from fastapi import APIRouter, Depends

from hackathon.web.api.auth.views import get_current_user
from hackathon.web.api.user.services import UserService

from .schema import *

router = APIRouter()


@router.get("/me")
async def get_me(
    user: UserBase = Depends(get_current_user),
    user_service: UserService = Depends(),
):
    return await user_service.get_user_by_id(user.id)


@router.get("/")
async def get_users(
    user: UserBase = Depends(get_current_user),
    user_service: UserService = Depends(),
) -> list[UserBase]:
    return await user_service.get_users()


@router.get("/positions")
async def get_positions(
    user_service: UserService = Depends(),
) -> list[PositionBase]:
    return await user_service.get_positions()
