from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        

def get_users_by_name(db: Session, name: str):
    return db.query(User).filter(User.username == name).all()