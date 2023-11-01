from pydantic import BaseModel

class Database(BaseModel):
    username: str
    db_name: str
    password: str

