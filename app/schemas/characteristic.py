from pydantic import BaseModel
from typing import Optional


class CharacteristicBase(BaseModel):
    name: Optional[str] = None

class CharacteristicCreate(CharacteristicBase):
    name: str

class CharacteristicResponse(CharacteristicBase):
    id: int
    name: Optional[str] = None

    class Config:
        orm_mode = True

class CharacteristicUpdate(BaseModel):
    name: Optional[str] = None
