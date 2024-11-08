from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.api.schemas.comment import CommentCreate, CommentUpdate
from app.models import Comment
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_post_comments(db: Session, post_id: str): 
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments
        
        
def create_comment(db: Session, comment: CommentCreate):
    db_comment = Comment(
        content=comment.content,
        user_name=comment.user_name,
        likes=comment.likes,
        post_id=comment.post_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
        
        
        
def delete_comment(db: Session, comment_id: str):
    db.query(Comment).filter(Comment.id == comment_id).delete()
    db.commit()
    return {"message": "Comment deleted"}

