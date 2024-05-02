from fastapi import APIRouter, HTTPException, Depends
from fastapi_users import FastAPIUsers

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import auth_backend, current_user
from src.auth.models import User
from src.database import get_async_session
from src.auth.manager import get_user_manager

from src.config import DB_HOST, DB_PORT
from src.models.models import connection
import psycopg2

router = APIRouter(
    prefix="/database",
    tags=["database"],
)

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self, dbname: str, user_id: int):
        new_database = f"{dbname}_{user_id}"
        self.connection = new_database

database_connection = DatabaseConnection()

@router.post("/create_db_server/{new_connect.database}") # создание БД(наверное)
async def create_db_server(new_database: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="You need to be logged in to create a server")

    conn = psycopg2.connect(
        dbname = 'websql',
        user = 'postgres',
        password = 'postgres',
        host = DB_HOST,
        port = DB_PORT
    )

    new_database_concat = "_".join([new_database, str(user.id)]) # костыль, если два юзера одинаково назовут бд

    try:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("CREATE DATABASE " + new_database_concat)
        conn.close()  # Закрываем соединение

    except Exception:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "details": "Такая БД уже существует"
        })

    stmt = insert(connection).values(id = user.id, database =new_database_concat)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success",
            "details": "Создана база данных " + new_database
            }

@router.post("/connect_to_db/")
async def connect_to_db(dbname: str, user: User = Depends(current_user)):
    try:
        database_connection.connect(dbname, user.id)
        return {"status": "success",
                "details": "Вы подключены к базе данных " + database_connection.connection}
    except Exception:
        raise HTTPException(status_code=489, detail={
            "status": "error",
            "details": "Такой базы данных не существует",
        })