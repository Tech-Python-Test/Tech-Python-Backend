from pydantic import BaseModel

class ConversationBase(BaseModel):
    user1_id: int
    user2_id: int

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: int

    class Config:
        orm_mode = True
