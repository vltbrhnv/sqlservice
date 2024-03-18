import json
from datetime import time, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, null, insert, text
from sqlalchemy.ext.asyncio import AsyncSession, async_session, create_async_engine
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from auth.database import get_async_session, engine
from models.models import connection, query
from service.schemas import ConnectionCreate


router = APIRouter(
    prefix="/users",
    tags=["User"]
)









