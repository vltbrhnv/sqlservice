from typing import Annotated, Sequence

import jwt
from fastapi import Depends, Header
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy, BearerTransport)
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.config import SECRET_AUTH

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

async def get_current_user(token: Annotated[str, Header()]) -> int:
    payload = jwt.decode(jwt=token, key= SECRET_AUTH,audience=["fastapi-users:auth"], algorithms="HS256", verify=True)
    print(f'PAYLoAD____Get_current_user_{payload}')
    return  int(payload.get("sub"))