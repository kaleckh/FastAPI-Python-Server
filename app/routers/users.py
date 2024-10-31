from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, models


router = APIRouter()

@router.get("/users")
def read_users(name: str, db: Session = Depends(get_db)):
    users = crud.get_users_by_name(db, name)
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users
