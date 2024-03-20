from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("firstname", String, nullable=False),
    Column("lastname", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False)
)

job = Table(
    "job",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("min_salary", Integer, nullable=False),
    Column("max_salary", Integer, nullable=False),
)

employee = Table(
    "employee",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("name", String, nullable=False),
    Column("phone_number", Integer, nullable=False),
    Column("salary", Integer, nullable=False),
    Column("job_id", Integer, ForeignKey("job.id"))
)

connection = Table(
    "connection",
    metadata,
    Column("hostname", String, nullable = False),
    Column("portname", Integer, nullable = False),
    Column("servername", String, nullable = False),
    Column("username", String, default="postgres", nullable = False),
    Column("database", String, default="postgres", nullable = False),
    Column("password", String, nullable = False),

)

query = Table(
    "query",
    metadata,
    Column("id", Integer, nullable=False),
    Column("queryname", String, nullable = False),
    Column("time", String, nullable = False),
)


