from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.api.schemas.posts import PostCreate, PostUpdate
from app.models import Post
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def get_posts(db: Session):
    return db.query(Post).all()


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def create_post(db: Session, post: PostCreate):
    db_post = Post(
        content=post.content,
        user_name=post.user_name,
        likes=post.likes,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post



def update_post(db: Session, post_id: int, post: PostUpdate):
    post_data = post.model_dump(exclude_unset=True)
    db.query(Post).filter(Post.id == post_id).update(post_data)
    db.commit()
    updated_post = db.query(Post).filter(Post.id == post_id).first()
    return updated_post



def delete_post(db: Session, post_id: int):
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()
    return {"message": "Post deleted"}