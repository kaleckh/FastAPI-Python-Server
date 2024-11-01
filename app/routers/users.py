from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, models


router = APIRouter()

@router.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return {"users": users}


@router.get("/user/{user_id}")
def read_user(user_id: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}
