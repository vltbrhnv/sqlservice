from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import text, insert, desc
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from auth.auth import auth_backend
from auth.database import get_async_session, User
from auth.manager import get_user_manager
from config import DB_PASS, DB_HOST, DB_PORT
from models.models import query

router = APIRouter()
"""
@router.post("/query") # написать sql запрос
async def get_query(sqlquery: str, database: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="You need to be logged in to make a query")

    DB_NAME = "_".join([database,str(user.id)])
    DB_USER = "postgres"
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    engine_db1 = create_async_engine(DATABASE_URL)
    async_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine_db1)
    session_db1 = async_session_maker()

    result =  await session_db1.execute(text(sqlquery))

    data = []
    keys = result.keys()
    for row in result.all():
        data.append({k: v for k, v in zip(keys, row)})
    timestamp = datetime.now()
    time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    add_query = insert(query).values(queryname = sqlquery,time = time_str, id = user.id)
    await session.execute(add_query)
    await session.commit()
    return {
        "status": "success",
        "data": data,
    }
@router.get("/get_queries") # получение истории запросов пользователя
async def get_user(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user),limit:int = 15):
    from sqlalchemy import select
    result = await session.execute(select(query).where(query.c.id == user.id).order_by(desc(query.c.time)))
    items = result.all()
    return {"status":"success",
            "data":[{"queryname": row.queryname ,"time": row.time, "id":row.id} for row in items][0:][:limit]}"""