from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from hackathon.db.dependencies import get_db_session
from hackathon.db.models.user import Position, User


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_user_by_id(self, id: int) -> User | None:
        user = await self.session.execute(
            select(User)
            .where(User.id == id)
            .options(selectinload(User.positions))
            .options(selectinload(User.team))
            .options(selectinload(User.team_applications))
        )
        return user.scalar_one_or_none()

    async def get_users(self) -> list[User]:
        users = await self.session.execute(
            select(User)
            .options(selectinload(User.positions))
            .options(selectinload(User.team))
            .options(selectinload(User.team_applications))
        )
        return list(users.scalars().all())

    async def get_positions(self) -> list[Position]:
        positions = await self.session.execute(select(Position))
        return list(positions.scalars().all())
