from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User
from fastapi import FastAPI, Depends
from app.schemas import UserCreate

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


def create_user(db: Session, user: UserCreate):    
    db_user = User(
        email=user.email,
        username=user.username,
        blurhash=user.blurhash,
        location=user.location,
        bio=user.bio,
        color=user.color,
        links=user.links,
        followers=user.followers,
        following=user.following,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user) 
    return db_user
