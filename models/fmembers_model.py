from pydantic import BaseModel

class UpdateFamilyMember(BaseModel):
    relationship_label: str | None = None
    avatar_url: str | None = None
