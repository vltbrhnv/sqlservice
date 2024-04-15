from datetime import datetime
from typing import AsyncGenerator

import psycopg2
from fastapi_users import FastAPIUsers
from fastapi import FastAPI, Depends, HTTPException
from psycopg2 import Error

from sqlalchemy import select, insert, text, desc, create_engine, MetaData, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

from auth.auth import auth_backend
from auth.database import User, get_async_session, Base
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from config import DB_PASS, DB_HOST, DB_PORT

from models.models import user, connection, query, Connection
from models.schemas import ConnectionCreate

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
        return {"status":"success",
                "data": [{"email": row.email,"username:": row.username,
                          "lastname": row.lastname, "firstname": row.firstname,
                          "password": row.hashed_password}]
               }
"""@app.post("/add_connection")
async def add_connection(new_connect: ConnectionCreate, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="You need to be logged in to create a server")

    stmt = insert(connection).values(**new_connect.dict())

    await session.execute(stmt)
    await session.commit()
    return {"status": "success",
            "servername":new_connect.servername
            }"""
@app.post("/create_db_server/") # создание БД
async def create_db_server(new_connect: ConnectionCreate,session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="You need to be logged in to create a server")

    conn = psycopg2.connect(
        dbname = 'websql',
        user = 'postgres',
        password = 'postgres',
        host = DB_HOST,
        port = DB_PORT
    )
    new_database = "_".join([new_connect.database,str(user.id)]) # костыль, если два юзера одинаково назовут бд
    try:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("CREATE DATABASE " + new_database)
        conn.close()  # Закрываем соединение
    except Exception:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "details": "Такая БД уже существует"
        })

    stmt = insert(connection).values(id = user.id, hostname = DB_HOST,portname = int(DB_PORT),
                                     servername = 'websql',username = user.username,database =new_connect.database, password = DB_PASS )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success",
            "dbname": new_connect.database
            }

@app.post("/query")
async def get_query(sqlquery: str, database: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="You need to be logged in to make a query")
    DB_NAME = "_".join([database,str(user.id)])
    DB_USER = "postgres"
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine_db1 = create_async_engine(DATABASE_URL)
    async_session_maker = sessionmaker(engine_db1, class_=AsyncSession, expire_on_commit=False)
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
@app.post("/connect_to_db/")
async def connect_to_db(dbname:str,user: User = Depends(current_user)):
    try:
        new_database = "_".join(["dbapril", str(user.id)])  # костыль, если два юзера одинаково назовут бд
        # Подключение к существующей базе данных
        connection_db = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database=new_database)
        # Курсор для выполнения операций с базой данных
        cursor = connection_db.cursor()
        print("Информация о сервере PostgreSQL")
        print(connection_db.get_dsn_parameters(), "\n")
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


@app.get("/ge_queries")
async def get_user(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user),limit:int = 15):
    result = await session.execute(select(query).where(query.c.id == user.id).order_by(desc(query.c.time)))
    items = result.all()
    return {"status":"success",
            "data":[{"queryname": row.queryname ,"time": row.time, "id":row.id} for row in items][0:][:limit]}
