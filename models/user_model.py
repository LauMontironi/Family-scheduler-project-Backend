from pydantic import BaseModel 
from datetime import date


class User(BaseModel):
    id: int 
    email:str  
    password: str 
    full_name:str
    created_at: date

class UserCreate(BaseModel):

    email:str  
    password: str 
    full_name:str

    
class UserLogin(BaseModel):
    email: str
    password: str