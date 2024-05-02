from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import declarative_base

from src.database import metadata

# user = Table(
#     "user",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("email", String, nullable=False),
#     Column("username", String, nullable=False),
#     Column("firstname", String, nullable=False),
#     Column("lastname", String, nullable=False),
#     Column("hashed_password", String, nullable=False),
#     Column("registered_at", TIMESTAMP, default=datetime.utcnow),
#     Column("is_active", Boolean, default=True, nullable=False),
#     Column("is_superuser", Boolean, default=False, nullable=False),
#     Column("is_verified", Boolean, default=False, nullable=False)
# )

connection = Table(
    "connection",
    metadata,
    Column("id", Integer, nullable = False),
    Column("database", String, nullable = False),
)

query = Table(
    "query",
    metadata,
    Column("id", Integer, nullable=False),
    Column("queryname", String, nullable = False),
    Column("time", String, nullable = False),
)


