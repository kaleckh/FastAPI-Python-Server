from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.api.schemas.comment import CommentCreate, CommentUpdate
from app.models import Comment
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_single_comment(db: Session, comment_id: str): 
    comments = db.query(Comment).filter(Comment.id == comment_id).all()
    return comments


def get_post_comments(db: Session, post_id: str): 
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments


def add_like(db: Session, post_id: str, user_id: str):
    try:
        comment = db.query(Comment).filter(Comment.id == post_id).first()

        if not comment:
            return None

        current_likes = comment.likes or []
        
        if user_id in current_likes:
            current_likes.remove(user_id)
        else:            
            current_likes.append(user_id)

        comment.likes = current_likes
        flag_modified(comment, "likes")
        db.commit()        
        db.refresh(comment)        
        return comment
    except Exception as e:
        raise


        
def create_comment(db: Session, comment: CommentCreate):
    db_comment = Comment(
        content=comment.content,
        user_name=comment.user_name,
        post_id=comment.post_id,        
        user_id=comment.user_id,        
        parent_id=comment.parent_id,         
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
        
        
        
def delete_comment(db: Session, comment_id: str):
    db.query(Comment).filter(Comment.id == comment_id).delete()
    db.commit()
    return {"message": "Comment deleted"}

