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

from .test_auth import test_sign_up_in


@pytest.mark.anyio
async def test_team_creation(
    dbsession: AsyncSession,
) -> tuple[UserBase, TeamBase]:
    team_repository = TeamRepository(dbsession)
    user_repository = UserRepository(dbsession)
    team_service = TeamService(
        user_repository=user_repository, team_repository=team_repository
    )

    user = await test_sign_up_in(dbsession)

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
    return user, created_team


@pytest.mark.anyio
async def test_apply_team(
    dbsession: AsyncSession,
) -> None:
    team_repository = TeamRepository(dbsession)
    user_repository = UserRepository(dbsession)
    team_service = TeamService(
        user_repository=user_repository, team_repository=team_repository
    )

    owner, created_team = await test_team_creation(dbsession)

    member = await test_sign_up_in(dbsession)

    res = await team_service.apply_to_team(
        team_id=created_team.id,
        user=member,
        comment=uuid.uuid4().hex,
    )
    assert res.success is True

    with pytest.raises(HTTPException):
        # can't apply twice
        await team_service.apply_to_team(
            team_id=created_team.id,
            user=member,
            comment=uuid.uuid4().hex,
        )

    team = await team_service.get_team_by_id(created_team.id)
    assert member.id not in team.members

    with pytest.raises(HTTPException):
        # can't accept if not member of the team
        await team_service.accept_user(
            team_id=created_team.id,
            user_id=member.id,
            me=member,
        )

    res = await team_service.accept_user(
        team_id=created_team.id,
        user_id=member.id,
        me=owner,
    )
    assert res.success is True

    team = await team_service.get_team_by_id(created_team.id)
    assert member.id in team.members


@pytest.mark.anyio
async def test_dismiss_user(
    dbsession: AsyncSession,
) -> None:
    team_repository = TeamRepository(dbsession)
    user_repository = UserRepository(dbsession)
    team_service = TeamService(
        user_repository=user_repository, team_repository=team_repository
    )

    owner, created_team = await test_team_creation(dbsession)

    member = await test_sign_up_in(dbsession)

    await team_service.apply_to_team(
        team_id=created_team.id,
        user=member,
        comment=uuid.uuid4().hex,
    )

    with pytest.raises(HTTPException):
        # can't dismiss if not member of the team
        await team_service.dismiss_user(
            team_id=created_team.id,
            user_id=member.id,
            me=member,
        )

    await team_service.dismiss_user(
        team_id=created_team.id,
        user_id=member.id,
        me=owner,
    )

    with pytest.raises(HTTPException):
        # already dismissed
        await team_service.accept_user(
            team_id=created_team.id,
            user_id=member.id,
            me=owner,
        )

    team = await team_service.get_team_by_id(created_team.id)
    assert member.id not in team.members
