from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hackathon.db.dependencies import get_db_session
from hackathon.db.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_user_by_id(self, id: int) -> User | None:
        user = await self.session.execute(select(User).where(User.id == id))
        return user.scalar_one_or_none()

    async def get_users(self) -> list[User]:
        users = await self.session.execute(select(User))
        return list(users.scalars().all())
