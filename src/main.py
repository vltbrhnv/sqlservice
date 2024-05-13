from fastapi_users import FastAPIUsers
from fastapi import FastAPI

from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate

from src.routers.router_query import router as router_query
from src.routers.router_database import router as router_database
from src.routers.router_user import router as router_user

app = FastAPI(
    title="SQL service"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_query)
app.include_router(router_database)
app.include_router(router_user)


