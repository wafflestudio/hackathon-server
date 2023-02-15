from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from hackathon.web.api.auth.services import AuthService

from .schema import *

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


@router.post("/signup", response_model=SignInResponse)
async def sign_up(
    sign_up_request: SignUpRequest,
    auth_service: AuthService = Depends(),
) -> SignInResponse:
    """Sign up new user."""
    return await auth_service.sign_up(sign_up_request)


@router.post("/signin", response_model=SignInResponse)
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
) -> SignInResponse:
    """Sign in user."""
    return await auth_service.sign_in(
        SignInRequest(username=form_data.username, password=form_data.password),
    )


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    response = await auth_service.sign_in(
        SignInRequest(username=form_data.username, password=form_data.password),
    )
    return {"access_token": response.token, "token_type": "bearer"}


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(),
):
    return await auth_service.get_current_user(token)
