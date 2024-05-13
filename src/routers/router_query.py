from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Header

from sqlalchemy import text, insert, desc, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.auth.auth import get_current_user
from src.database import get_async_session
from src.config import DB_PASS, DB_HOST, DB_PORT, DB_USER
from src.models.models import query
from src.routers.router_database import database_name

router = APIRouter(
    prefix="/query",
    tags=["query"],
)
@router.get("/query")
async def get_query(sqlquery: str, session: AsyncSession = Depends(get_async_session),
                    user: int = Depends(get_current_user), token: Annotated[str, Header()]=None):
    if not user:
        raise HTTPException(status_code=401, detail="You need to be logged in to make a query")

    DB_NAME = database_name.get_database_name()

    if DB_NAME == "default":
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "details": "Вы не подключены к базе данных"
        })

    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine_db1 = create_async_engine(DATABASE_URL)
    async_session_maker = sessionmaker(engine_db1, class_=AsyncSession, expire_on_commit=False)
    session_db = async_session_maker() # создание сессии для выполнения запросов в БД пользователя
    try:
        timestamp = datetime.now()
        time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        queries = sqlquery.split(';')  # разделяем SQL-запросы
        data = []
        for q in queries:
            if q.strip():  # Пропуск пустых запросов
                result = await session_db.execute(text(q))  # Выполнение отдельного SQL-запроса
                if 'CREATE' in q:
                    data.append("Таблица была успешна создана")
                if 'INSERT' in q:
                    data.append("В таблицу были успешно добaвлены данные")
                if 'DELETE' in q:
                    data.append("Из таблицы был успешно удален столбец")
                if  'SELECT' in q:
                    keys = result.keys()
                    for row in result.all():
                        data.append({k: v for k, v in zip(keys, row)})
        await session_db.commit()
        add_query = insert(query).values(queryname=sqlquery, time=time_str, id=user)
        await session.execute(add_query)
        await session.commit()
        return {
            "status": "success",
            "data": data,
        }
    except Exception as e:
        return {
            "status": "error",
            "details": str(e)
        }

@router.get("/query_history/{user_id}") # получение истории запросов пользователя
async def get_user(session: AsyncSession = Depends(get_async_session), user: int = Depends(get_current_user),limit:int = 15):

    result = await session.execute(select(query).where(query.c.id == user).order_by(desc(query.c.time)))
    items = result.all()
    return {"status":"success",
            "data":[{"queryname": row.queryname ,"time": row.time, "id":row.id} for row in items][0:][:limit]}