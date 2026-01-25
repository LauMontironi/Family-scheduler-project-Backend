from pydantic import BaseModel 
from datetime import date, datetime
from typing import Optional 

class CreateFamily(BaseModel):
    name:str

class UpdateFamily(BaseModel):
    id:int
    name:str 