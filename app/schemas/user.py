from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    profile_picture: Optional[HttpUrl] = None
    interests: Optional[str] = None
    skills: Optional[str] = None
    social_links: Optional[str] = None

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    profile_picture: Optional[HttpUrl] = None
    interests: Optional[str] = None
    skills: Optional[str] = None
    social_links: Optional[str] = None
