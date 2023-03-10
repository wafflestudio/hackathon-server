from fastapi import Depends, HTTPException

from hackathon.web.api.team.repositories import TeamRepository
from hackathon.web.api.team.schema import (
    TeamApplicationBase,
    TeamBase,
    TeamCreateRequest,
    TeamDetail,
    TeamOperationResult,
)
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

    async def get_team_by_id(self, team_id: int) -> TeamDetail:
        team = await self.team_repository.get_team_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return TeamDetail(
            id=team.id,
            name=team.name,
            resolution=team.resolution,
            maxMembers=team.max_members,
            members=[
                UserBase(
                    id=member.id,
                    username=member.username,
                    fullname=member.fullname,
                    positions=[position.name for position in member.positions],
                    team_id=member.team_id,
                )
                for member in team.members
            ],
            applications=[
                TeamApplicationBase(
                    id=application.id,
                    comment=application.comment,
                    team_id=application.team_id,
                    user=UserBase(
                        id=application.user.id,
                        username=application.user.username,
                        fullname=application.user.fullname,
                        positions=[
                            position.name for position in application.user.positions
                        ],
                        team_id=application.user.team_id,
                    ),
                )
                for application in team.team_applications
            ],
        )

    async def get_teams(self) -> list[TeamBase]:
        teams = await self.team_repository.get_teams()
        return [team.to_pydantic() for team in teams]

    async def create_team(self, data: TeamCreateRequest, user: UserBase) -> TeamDetail:
        if (
            user_model := await self.user_repository.get_user_by_id(user.id)
        ) and user_model.is_tester:
            raise HTTPException(status_code=400, detail="Testers can't create team")

        team = await self.team_repository.create_team(
            name=data.name,
            user_id=user.id,
            resolution=data.resolution,
            max_members=data.maxMembers,
        )
        if not (1 < data.maxMembers <= 4):
            raise HTTPException(
                status_code=400, detail="Max members must be between 2 and 4"
            )
        if not team:
            raise HTTPException(status_code=400, detail="Team creation failed")
        return TeamDetail(
            id=team.id,
            name=team.name,
            resolution=team.resolution,
            maxMembers=team.max_members,
            members=[
                UserBase(
                    id=member.id,
                    username=member.username,
                    fullname=member.fullname,
                    positions=[position.name for position in member.positions],
                    team_id=member.team_id,
                )
                for member in team.members
            ],
            applications=[
                TeamApplicationBase(
                    id=application.id,
                    comment=application.comment,
                    team_id=application.team_id,
                    user=UserBase(
                        id=application.user.id,
                        username=application.user.username,
                        fullname=application.user.fullname,
                        positions=[
                            position.name for position in application.user.positions
                        ],
                        team_id=application.user.team_id,
                    ),
                )
                for application in team.team_applications
            ],
        )

    async def apply_to_team(
        self,
        team_id: int,
        user: UserBase,
        comment: str,
    ) -> TeamOperationResult:
        user_model = await self.user_repository.get_user_by_id(user.id)
        if user_model and user_model.is_tester:
            raise HTTPException(
                status_code=400, detail="Testers can't apply for a team."
            )
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

    async def delete_team(self, team_id: int) -> TeamOperationResult:
        await self.team_repository.delete_team(team_id)
        return TeamOperationResult(success=True)
