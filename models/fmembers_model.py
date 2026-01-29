from pydantic import BaseModel
from datetime import date
from typing import Optional

class MemberBase(BaseModel):
    full_name: str
    relationship: str # madre, padre, hijo...
    is_child: bool = False
    birthdate: Optional[date] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    hobbys: Optional[str] = None

class MemberCreate(MemberBase):
    email: Optional[str] = None # Solo si es adulto
    password: Optional[str] = None # Solo si es adulto

class MemberResponse(MemberBase):
    id: int
    family_id: int

class UpdateFamilyMember(BaseModel):
    relationship: Optional[str] = None
    hobbys: Optional[str] = None
    city: Optional[str] = None
    gender: Optional[str] = None