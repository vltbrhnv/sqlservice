from pydantic import BaseModel
class ConnectionCreate(BaseModel):
    hostname: str
    portname: int = 5432
    servername: str
    username: str = "postgres"
    database: str = "postgres"
    password: str