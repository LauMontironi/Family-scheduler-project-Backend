from pydantic import BaseModel 
from datetime import date, datetime
from typing import Optional 

class CreateChild(BaseModel):
    name: str
    birthdate: date | None = None
    notes: str | None = None

class modifyChild(CreateChild):
    id:int