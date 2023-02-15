from fastapi import Depends, HTTPException

from hackathon.web.api.team.repositories import TeamRepository
from hackathon.web.api.team.schema import TeamBase
from hackathon.web.api.user.repositories import UserRepository


class TeamService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        team_repository: TeamRepository = Depends(),
    ):
        self.user_repository = user_repository
        self.team_repository = team_repository

    async def get_team_by_id(self, team_id: int) -> TeamBase:
        team = await self.team_repository.get_team_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return team.to_pydantic()

    async def get_teams(self) -> list[TeamBase]:
        teams = await self.team_repository.get_teams()
        return [team.to_pydantic() for team in teams]
