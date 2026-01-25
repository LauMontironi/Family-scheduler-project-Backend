from pydantic import BaseModel 
from datetime import date, datetime
from typing import Optional 

class UserCreate(BaseModel):
    email:str
    password:str
    full_name:str