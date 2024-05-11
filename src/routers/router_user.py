from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.auth.auth import get_current_user
from src.auth.models import user, User
from src.database import get_async_session

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get("/get_user_info/")
async def get_user(token: Annotated[str, Header()]=None,
                   session: AsyncSession = Depends(get_async_session), my_user: int = Depends(get_current_user)):
    stmt = select(user).where(user.c.id == my_user)
    result = await session.execute(stmt)
    row = result.fetchone()
    if row is None:
        return {"error": "User not found"}
    return {"status": "success",
            "data": [{"email": row.email, "username:": row.username,
                      "lastname": row.lastname, "firstname": row.firstname}]
            }
