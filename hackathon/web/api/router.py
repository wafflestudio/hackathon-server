from fastapi.routing import APIRouter

from hackathon.web.api import auth, docs, team, user

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(team.router, prefix="/teams", tags=["team"])
api_router.include_router(user.router, prefix="/users", tags=["user"])
