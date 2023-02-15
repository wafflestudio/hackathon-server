from fastapi import Depends, HTTPException

from hackathon.web.api.team.repositories import TeamRepository
from hackathon.web.api.team.schema import TeamBase, TeamCreate, TeamOperationResult
from hackathon.web.api.user.repositories import UserRepository
from hackathon.web.api.user.schema import UserBase


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

    async def create_team(self, data: TeamCreate, user: UserBase) -> TeamBase:
        team = await self.team_repository.create_team(
            name=data.name,
            user_id=user.id,
            resolution=data.resolution,
            max_members=data.maxMembers,
        )
        return team.to_pydantic()

    async def apply_to_team(
        self,
        team_id: int,
        user: UserBase,
        comment: str,
    ) -> TeamOperationResult:
        await self.team_repository.apply_team(team_id, user.id, comment)
        return TeamOperationResult(success=True)

    async def cancel_application(
        self,
        team_id: int,
        me: UserBase,
    ) -> TeamOperationResult:
        await self.team_repository.cancel_application(team_id, me.id)
        return TeamOperationResult(success=True)

    async def leave_team(self, team_id: int, me: UserBase):
        await self.team_repository.leave_team(team_id, me.id)
        return TeamOperationResult(success=True)

    async def accept_user(
        self,
        team_id: int,
        user_id: int,
        me: UserBase,
    ) -> TeamOperationResult:
        if not (
            await self.team_repository.is_user_in_team(user_id=me.id, team_id=team_id)
        ):
            raise HTTPException(status_code=403, detail="You are not in this team")
        await self.team_repository.accept_user(team_id, user_id)
        return TeamOperationResult(success=True)

    async def dismiss_user(
        self,
        team_id: int,
        user_id: int,
        me: UserBase,
    ) -> TeamOperationResult:
        if not (
            await self.team_repository.is_user_in_team(user_id=me.id, team_id=team_id)
        ):
            raise HTTPException(status_code=403, detail="You are not in this team")
        await self.team_repository.cancel_application(team_id, user_id)
        return TeamOperationResult(success=True)

    async def kick_user(
        self,
        team_id: int,
        user_id: int,
        me: UserBase,
    ) -> TeamOperationResult:
        if not (
            await self.team_repository.is_user_in_team(user_id=me.id, team_id=team_id)
        ):
            raise HTTPException(status_code=403, detail="You are not in this team")
        await self.team_repository.leave_team(team_id, user_id)
        return TeamOperationResult(success=True)
