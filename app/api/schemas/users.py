from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# Base schema for common fields
class UserBase(BaseModel):
    email: EmailStr
    username: str
    blurhash: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    color: Optional[str] = None
    links: Optional[str] = None
    followers: List[str] = []
    following: List[str] = []
    

# Schema for creating a new user
class UserCreate(UserBase):
    pass  # No extra fields are required beyond UserBase

class UserUpdate(UserBase):
    pass  # No extra fields are required beyond UserBase

# Schema for responding with user data
class UserResponse(UserBase):
    id: str
    date: datetime

    class Config:
        orm_mode = True  # Enable ORM mode to work with SQLAlchemy
