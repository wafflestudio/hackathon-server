from fastapi import APIRouter, Depends

from hackathon.db.models.user import User
from hackathon.web.api.auth.views import get_current_user
from hackathon.web.api.team.services import TeamService

from .schema import *

router = APIRouter()


@router.get("/")
async def get_teams(
    user: User = Depends(get_current_user),
    team_service: TeamService = Depends(),
) -> list[TeamBase]:
    return await team_service.get_teams()


@router.get("/{team_id}")
async def get_team(
    team_id: int,
    user: User = Depends(get_current_user),
    team_service: TeamService = Depends(),
) -> TeamBase:
    return await team_service.get_team_by_id(team_id)


# @router.post("/")
