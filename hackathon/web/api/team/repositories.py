from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from hackathon.db.dependencies import get_db_session
from hackathon.db.models.team import Team


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

    async def apply_team(self, team_id: int, user_id: int) -> None:
        pass
