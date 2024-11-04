from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.models import User
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        

def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(user: schemas.UserCreate, db: Session = Depends(get_db) ):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

