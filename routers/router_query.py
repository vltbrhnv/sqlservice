from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import text, insert, desc, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from auth.auth import auth_backend
from auth.database import get_async_session, User
from auth.manager import get_user_manager
from config import DB_PASS, DB_HOST, DB_PORT, DB_USER

from models.models import query

from routers.router_database import database_connection

router = APIRouter(
    prefix="/query",
    tags=["query"],
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

@router.post("/query") # написать sql запрос
async def get_query(sqlquery: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="You need to be logged in to make a query")

    DB_NAME = database_connection.connection
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    try:
        engine_db1 = create_async_engine(DATABASE_URL)
        async_session_maker = sessionmaker(engine_db1, class_=AsyncSession, expire_on_commit=False)
        session_db1 = async_session_maker()
        timestamp = datetime.now()
        time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        add_query = insert(query).values(queryname=sqlquery, time=time_str, id=user.id)
        await session.execute(add_query)
        await session.commit()
        await session_db1.commit()
        if sqlquery.count(';') <= 1:
            result = await session_db1.execute(text(sqlquery))

            if 'CREATE' in sqlquery:
                try:
                    return {
                        "status": "success",
                        "details": "Таблица была успешна создана"
                    }
                except Exception as e:
                    return{
                        "status": "error",
                        "details": str(e)
                    }
            elif 'INSERT' in sqlquery:
                print('*')
                try:
                    return {
                        "status": "success",
                        "details": "В таблицу были успешно добавлены столбцы"
                    }
                except Exception as e:
                    return{
                        "status": "error",
                        "details": str(e)
                    }
            elif 'DELETE' in sqlquery:
                print('*')
                try:
                    return {
                        "status": "success",
                        "details": "Столбцы были успешно удалены"
                    }
                except Exception as e:
                    return{
                        "status": "error",
                        "details": str(e)
                    }
            else:
                data = []
                keys = result.keys()
                for row in result.all():
                    data.append({k: v for k, v in zip(keys, row)})

                return {
                    "status": "success",
                    "data": data,
                }
        else:

            queries = sqlquery.split(';')  # Разделение SQL-запросов по точке с запятой
            for q in queries:
                if q.strip():  # Пропуск пустых запросов
                    await session_db1.execute(text(q.strip()))  # Выполнение отдельного SQL-запроса
            await session_db1.commit()

            return{
                "status": "success",
                "details": "Запросы успешно выполнены"
            }

    except Exception as e:
        return {
            "status": "error",
            "details": str(e),
        }

@router.get("/query_history/{user_id}") # получение истории запросов пользователя
async def get_user(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user),limit:int = 15):

    result = await session.execute(select(query).where(query.c.id == user.id).order_by(desc(query.c.time)))
    items = result.all()
    return {"status":"success",
            "data":[{"queryname": row.queryname ,"time": row.time, "id":row.id} for row in items][0:][:limit]}