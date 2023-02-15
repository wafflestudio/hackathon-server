from fastapi import APIRouter, Depends

from hackathon.web.api.auth.views import get_current_user
from hackathon.web.api.team.services import TeamService

from .schema import *

router = APIRouter()


@router.get("/")
async def get_teams(
    user: UserBase = Depends(get_current_user),
    team_service: TeamService = Depends(),
) -> list[TeamBase]:
    return await team_service.get_teams()


@router.get("/{team_id}")
async def get_team(
    team_id: int,
    user: UserBase = Depends(get_current_user),
    team_service: TeamService = Depends(),
) -> TeamBase:
    return await team_service.get_team_by_id(team_id)


@router.post("/")
async def create_team(
    data: TeamCreate,
    user: UserBase = Depends(get_current_user),
    team_service: TeamService = Depends(),
) -> TeamBase:
    return await team_service.create_team(data, user)


@router.post("/{team_id}/apply")
async def apply_to_team(
    team_id: int,
    data: TeamApplyRequest,
    user: UserBase = Depends(get_current_user),
    team_service: TeamService = Depends(),
):
    return await team_service.apply_to_team(team_id, user)


@router.delete("/{team_id}/apply")
async def cancel_application(
    team_id: int,
    user: UserBase = Depends(get_current_user),
    team_service: TeamService = Depends(),
):
    return await team_service.cancel_application(team_id, user)


@router.post("/{team_id}/leave")
async def leave_team(
    team_id: int,
    user: UserBase = Depends(get_current_user),
    team_service: TeamService = Depends(),
):
    return await team_service.leave_team(team_id, user)


@router.post("/{team_id}/dismiss/{user_id}")
async def dismiss_user(
    team_id: int,
    user_id: int,
    user: UserBase = Depends(get_current_user),
    team_service: TeamService = Depends(),
):
    return await team_service.dismiss_user(team_id, user_id, user)


@router.post("/{team_id}/accept/{user_id}")
async def accept_user(
    team_id: int,
    user_id: int,
    user: UserBase = Depends(get_current_user),
    team_service: TeamService = Depends(),
):
    return await team_service.accept_user(team_id, user_id, user)


@router.post("/{team_id}/kick/{user_id}")
async def kick_user(
    team_id: int,
    user_id: int,
    user: UserBase = Depends(get_current_user),
    team_service: TeamService = Depends(),
):
    return await team_service.kick_user(team_id, user_id, user)
