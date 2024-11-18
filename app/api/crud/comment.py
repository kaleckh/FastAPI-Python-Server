from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.api.schemas.comment import CommentCreate, CommentUpdate
from app.models import Comment
from sqlalchemy.exc import SQLAlchemyError
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


def add_like(db: Session, post_id: str, user_id: str):
    try:
        post = db.query(Comment).filter(Comment.id == post_id).first()
        if not post:
            return None  
        current_likes = post.likes or []
        
        if user_id in current_likes:
            current_likes.remove(user_id)
        else:
            current_likes.append(user_id)
        post.likes = current_likes
        db.commit()
        db.refresh(post)
        return post

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        db.rollback()
        raise
        
        
def create_comment(db: Session, comment: CommentCreate):
    db_comment = Comment(
        content=comment.content,
        user_name=comment.user_name,
        post_id=comment.post_id,
        likes=comment.likes
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
        
        
        
def delete_comment(db: Session, comment_id: str):
    db.query(Comment).filter(Comment.id == comment_id).delete()
    db.commit()
    return {"message": "Comment deleted"}

