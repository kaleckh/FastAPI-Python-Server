from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud import user as crud
from app.api.schemas.users import UserCreate, UserUpdate


router = APIRouter()


@router.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return {"users": users}



@router.get("/usernameCheck")
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)  
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/myInfo")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}


@router.post("/create")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db, user)    
    return {"user": user}


@router.put("/update/{user_id}")
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    user_data = user.model_dump(exclude_unset=True)
    user = crud.update_user(db, user_id, user_data)
    return {"user": user}


@router.delete("/delete/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    return {"user": user}
