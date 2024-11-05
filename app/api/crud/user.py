from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.api.schemas.users import UserCreate, UserUpdate
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


def create_user(db: Session, user: UserCreate):
    # Convert the Pydantic model instance to an SQLAlchemy model instance
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

    # Add the SQLAlchemy model instance to the database session
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Refresh to get the new data from the database
    return db_user

def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    db.query(User).filter(User.id == user_id).update(user)
    db.commit()
    return user


def delete_user(user_id: str, db: Session = Depends(get_db)):
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return {"message": "User deleted"}
