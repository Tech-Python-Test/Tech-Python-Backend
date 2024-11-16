from pydantic import BaseModel
from datetime import datetime

class GroupMessageBase(BaseModel):
    group_id: int
    sender_id: int
    content: str

class GroupMessageCreate(GroupMessageBase):
    pass

class GroupMessageResponse(GroupMessageBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
