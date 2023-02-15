from fastapi import APIRouter, Depends

from hackathon.db.models.user import User
from hackathon.web.api.auth.views import get_current_user

router = APIRouter()


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user.__dict__
