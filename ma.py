from datetime import datetime

from fastapi_users import FastAPIUsers
from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy import select, insert, text
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.database import User, get_async_session
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

from models.models import user, connection, query
from service.schemas import ConnectionCreate

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

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):

    return f"Hello, {user.username}"

@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"

@app.get("/get_user_info/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):

    query = select(user).where(user.c.id == user_id)
    result = await session.execute(query)
    row = result.fetchone()

    if row is None:
        return {"error": "User not found"}
    else:
        return {"email": row.email,"username:": row.username, "lastname": row.lastname, "firstname": row.firstname, "password": row.hashed_password}

@app.post("/add_connection")
async def add_connection(new_connect: ConnectionCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(connection).values(**new_connect.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@app.post("/query") # ДОДЕЛАТЬ НЕ РАБОТАЕТ ВЫВОД
async def get_query(sqlquery: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="You need to be logged in to access this endpoint")

    result = await session.execute(text(sqlquery))
    data = []
    keys = result.keys()
    for row in result.all():
        data.append({k: v for k, v in zip(keys, row)})
    timestamp = datetime.now()
    time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    add_q = text(f"insert into query values('{sqlquery}', '{time_str}', {user.id} )")
    await session.execute(add_q)
    await session.commit()

    return {
        "status": "success",
        "data": data,
        "details": None
    }

@app.get("/get_queries")
async def get_user(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    result = await session.execute(select(query).where(query.c.id == user.id))
    items = result.all()
    print(items)
    return [{"queryname": row.queryname ,"time": row.time, "id":row.id} for row in items]








