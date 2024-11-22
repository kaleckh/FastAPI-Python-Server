from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class RepostBase(BaseModel):
    post_id: str = None
    comment_id: str = None
    user_id: str


class RepostCreate(RepostBase):
    pass

class RepostUpdate(RepostBase):
    pass    

class RepostDelete(RepostBase):
    pass    

class RepostResponse(RepostBase):
    date: datetime

    class Config:
        orm_mode = True



