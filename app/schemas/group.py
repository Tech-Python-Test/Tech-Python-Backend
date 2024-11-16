from pydantic import BaseModel
from typing import List

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    member_ids: List[int]  # Lista de IDs de los usuarios para agregar al grupo

class GroupResponse(GroupBase):
    id: int

    class Config:
        orm_mode = True
