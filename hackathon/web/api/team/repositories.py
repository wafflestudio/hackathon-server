from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from hackathon.db.dependencies import get_db_session
from hackathon.db.models.team import Team
from hackathon.db.models.user import User


class TeamRepository:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_teams(self) -> list[Team]:
        teams = await self.session.execute(
            select(Team).options(
                selectinload(Team.members).options(selectinload(Team.applicants)),
            ),
        )
        return list(teams.scalars().all())

    async def get_team_by_id(self, id: int) -> Team | None:
        team = await self.session.execute(
            select(Team)
            .where(Team.id == id)
            .options(selectinload(Team.members).options(selectinload(Team.applicants))),
        )
        return team.scalar_one_or_none()

    async def is_user_in_team(self, user_id: int, team_id: int) -> bool:
        team = await self.session.execute(
            select(Team).where(Team.id == team_id).options(selectinload(Team.members)),
        )
        team = team.scalar_one_or_none()
        if not team:
            return False
        return any(user.id == user_id for user in team.members)

    async def create_team(
        self,
        name: str,
        user_id: int,
        resolution: str,
        max_members: int,
    ) -> Team:
        team = Team(name=name, resolution=resolution, max_members=max_members)
        owner = (
            await self.session.execute(select(User).where(User.id == user_id))
        ).scalar_one_or_none()
        if owner:
            team.members.append(owner)
        self.session.add(team)
        return team

    async def apply_team(self, team_id: int, user_id: int) -> None:
        team = await self.session.execute(select(Team).where(Team.id == team_id))
        team = team.scalar_one_or_none()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        user = await self.session.execute(select(User).where(User.id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user in team.applicants:
            raise HTTPException(status_code=400, detail="User already applied")
        team.applicants.append(user)

    async def cancel_application(self, team_id: int, user_id: int) -> None:
        team = await self.session.execute(select(Team).where(Team.id == team_id))
        team = team.scalar_one_or_none()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        user = await self.session.execute(select(User).where(User.id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user not in team.applicants:
            raise HTTPException(status_code=400, detail="User not applied")
        team.applicants.remove(user)

    async def accept_user(self, team_id: int, user_id: int) -> None:
        team = await self.session.execute(select(Team).where(Team.id == team_id))
        team = team.scalar_one_or_none()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        user = await self.session.execute(select(User).where(User.id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user not in team.applicants:
            raise HTTPException(status_code=400, detail="User not applied")
        team.applicants.remove(user)
        team.members.append(user)

    async def leave_team(self, team_id: int, user_id: int) -> None:
        team = await self.session.execute(select(Team).where(Team.id == team_id))
        team = team.scalar_one_or_none()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        user = await self.session.execute(select(User).where(User.id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user not in team.members:
            raise HTTPException(status_code=400, detail="User not in team")
        team.members.remove(user)

    async def delete_team(self, team_id: int) -> None:
        team = await self.session.execute(select(Team).where(Team.id == team_id))
        team = team.scalar_one_or_none()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        await self.session.delete(team)
