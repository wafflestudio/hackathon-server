import uuid

import pytest
from fastapi import FastAPI, HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from hackathon.web.api.auth.repositories import AuthRepository
from hackathon.web.api.auth.schema import SignInRequest, SignUpRequest
from hackathon.web.api.auth.services import AuthService

from hackathon.web.api.team.repositories import *
from hackathon.web.api.team.schema import *
from hackathon.web.api.team.services import *
from hackathon.web.api.user.services import UserService


@pytest.mark.anyio
async def test_team_creation(
    dbsession: AsyncSession,
) -> None:
    team_repository = TeamRepository(dbsession)
    user_repository = UserRepository(dbsession)
    auth_repository = AuthRepository(dbsession)
    team_service = TeamService(
        user_repository=user_repository, team_repository=team_repository
    )
    auth_service = AuthService(auth_repository)
    user_service = UserService(user_repository=user_repository)

    username = uuid.uuid4().hex
    password = uuid.uuid4().hex
    await auth_service.sign_up(
        data=SignUpRequest(
            fullname=uuid.uuid4().hex,
            username=username,
            password=password,
            positions=[],  # TODO: impl position
        )
    )
    response = await auth_service.sign_in(
        data=SignInRequest(
            username=username,
            password=password,
        )
    )

    assert response.token is not None

    user = await user_service.get_user_by_id(response.user.id)
    assert user.username == username

    await dbsession.commit()

    created_team = await team_service.create_team(
        data=TeamCreateRequest(
            name=(team_name := uuid.uuid4().hex),
            resolution=uuid.uuid4().hex,
            maxMembers=3,
        ),
        user=user,
    )
    await dbsession.commit()
    assert (await team_service.get_team_by_id(created_team.id)).name == team_name
