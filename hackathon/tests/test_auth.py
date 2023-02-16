import uuid

import pytest
from fastapi import FastAPI, HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from hackathon.web.api.auth.repositories import AuthRepository
from hackathon.web.api.auth.schema import *
from hackathon.web.api.auth.services import AuthService
from hackathon.web.api.user.repositories import UserRepository
from hackathon.web.api.user.services import UserService


@pytest.mark.anyio
async def test_sign_up_in(dbsession: AsyncSession) -> None:
    """Tests dummy instance creation."""
    auth_repository = AuthRepository(dbsession)
    user_repository = UserRepository(dbsession)
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


@pytest.mark.anyio
async def test_sign_up_in_fail(dbsession: AsyncSession) -> None:
    """Tests dummy instance creation."""
    auth_repository = AuthRepository(dbsession)
    auth_service = AuthService(auth_repository)
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
    with pytest.raises(HTTPException):
        await auth_service.sign_in(
            data=SignInRequest(
                username=username,
                password=password + "1",
            )
        )
