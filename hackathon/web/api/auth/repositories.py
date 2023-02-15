import bcrypt
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from hackathon.db.dependencies import get_db_session
from hackathon.db.models.user import Position, User


class AuthRepository:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def add_user(
        self,
        username: str,
        fullname: str,
        password: str,
        positions: list[str],
    ) -> None:
        position_models = await self.session.execute(
            select(Position).where(Position.name.in_(positions)),
        )

        # generate token based on username and password
        token = bcrypt.hashpw(
            (username + password).encode("utf-8"),
            bcrypt.gensalt(),
        )

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        )

        self.session.add(
            User(
                username=username,
                fullname=fullname,
                hashed_password=str(hashed_password, "utf-8"),
                token=str(token, "utf-8"),
                positions=position_models.all(),
            ),
        )

    async def get_user_by_username(self, username: str) -> User | None:
        user = await self.session.execute(
            select(User)
            .where(User.username == username)
            .options(selectinload(User.positions)),
        )
        return user.scalar_one_or_none()

    async def get_user_by_token(self, token: str) -> User | None:
        user = await self.session.execute(
            select(User)
            .where(User.token == token)
            .options(selectinload(User.positions)),
        )
        return user.scalar_one_or_none()
