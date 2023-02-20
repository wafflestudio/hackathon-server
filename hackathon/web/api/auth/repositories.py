import bcrypt
from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from hackathon.db.dependencies import get_db_session
from hackathon.db.models.user import Position, User


class AuthRepository:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def add_positions(self, positions: list[str]) -> None:
        values = [{"name": position} for position in positions]
        await self.session.execute(
            insert(Position).values(values).prefix_with("OR IGNORE")
        )

    async def add_user(
        self,
        username: str,
        fullname: str,
        password: str,
        positions: list[str],
        is_tester: bool = False,
    ) -> None:
        await self.add_positions(positions)
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
                is_tester=is_tester,
                hashed_password=str(hashed_password, "utf-8"),
                token=str(token, "utf-8"),
                positions=position_models.scalars().all(),
            ),
        )
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise e

    async def get_user_by_username(self, username: str) -> User | None:
        user = await self.session.execute(
            select(User)
            .where(User.username == username)
            .options(selectinload(User.positions))
            .options(selectinload(User.team))
            .options(selectinload(User.team_applications))
        )
        return user.scalar_one_or_none()

    async def get_user_by_token(self, token: str) -> User | None:
        user = await self.session.execute(
            select(User)
            .where(User.token == token)
            .options(selectinload(User.positions))
            .options(selectinload(User.team))
            .options(selectinload(User.team_applications))
        )
        return user.scalar_one_or_none()
