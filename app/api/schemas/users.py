from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# Base schema for common fields

class UserBase(BaseModel):
    email: EmailStr  # Required
    username: Optional[str] = None  # Required
    blurhash: Optional[str] = None  # Optional, default is None
    location: Optional[str] = None  # Optional, default is None
    bio: Optional[str] = None  # Optional, default is None
    color: Optional[str] = None  # Optional, default is None
    links: Optional[str] = None  # Optional, default is None
    followers: List[str] = []  # Optional, default is an empty list
    following: List[str] = []  # Optional, default is an empty list

# Schema for creating a new user
class UserCreate(UserBase):
    pass  # No extra fields are required beyond UserBase

class UserUpdate(UserBase):
    email: str
    location: str = None
    bio: str = None
    color: str = None
    links: str = None

class UserDelete(UserBase):
    user_id: str


# Schema for responding with user data
class UserResponse(UserBase):
    id: str
    date: datetime

    class Config:
        from_attributes = True  # Enable ORM mode to work with SQLAlchemy
