from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.api.schemas.repost import RepostCreate, RepostUpdate
from app.models import Repost
from fastapi import FastAPI, Depends


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def create_repost(db: Session, repost: RepostCreate):
    db_repost = Repost(
        post_id=repost.post_id,
        user_id=repost.user_id,
    )
    db.add(db_repost)
    db.commit()
    db.refresh(db_repost)
    return db_repost


def delete_repost(db: Session, user_id: str, post_id: str):
    db.query(Repost).filter(Repost.user_id == user_id and Repost.post_id == post_id).delete()
    db.commit()
    return {"message": "Repost deleted"}