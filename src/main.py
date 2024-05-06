from fastapi_users import FastAPIUsers
from fastapi import FastAPI

from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate

from src.routers.router_query import router as router_q
from src.routers.router_database import router as router_database
from src.routers.router_user import router as router_user

app = FastAPI(
    title="SQL service"
)
# логика для авторизации/регистрации пользователя
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

current_user = fastapi_users.current_user()

app.include_router(router_q)
app.include_router(router_database)
app.include_router(router_user)


