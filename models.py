from typing import Optional

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

class Database(BaseModel):
    name: str
    password: str

@dataclass
class Project(BaseModel):
    database: Database
    abs_media_dir: Optional[str]
