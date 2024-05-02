from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import auth_backend, current_user
from src.auth.models import User, user

from src.auth.manager import get_user_manager
from sqlalchemy import select

from src.database import get_async_session

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get("/get_user_info/{user_id}") # получаем информацию о пользователе
async def get_user(my_user = Depends(current_user), session: AsyncSession = Depends(get_async_session)):

    stmt = select(user).where(user.c.id == my_user.id)
    result = await session.execute(stmt)
    row = result.fetchone()
    if row is None:
        return {"error": "User not found"}
    return {"status":"success",
            "data": [{"email": row.email,"username:": row.username,
                      "lastname": row.lastname, "firstname": row.firstname}]
           }