from pydantic import BaseModel
class ConnectionCreate(BaseModel):
    database: str = "postgres"