from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm.attributes import flag_modified
from app.api.schemas.posts import PostCreate, PostUpdate
from app.models import Post, Repost, User, Comment
from fastapi import FastAPI, Depends
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def get_posts(db: Session):
    return db.query(Post).all()



from sqlalchemy.orm import Session, joinedload
from app.models import Post, Comment

def get_post(db: Session, post_id: str):
    # Fetch the post with comments that have no parent_id
    post = db.query(Post).filter(Post.id == post_id).options(
        joinedload(Post.comments)  # Eager load comments
        .joinedload(Comment.replies)  # Eager load replies for each comment
        .joinedload(Comment.user),  # Eager load user details for each comment
        joinedload(Post.reposts),  # Eager load reposts for the post
        joinedload(Post.comments).joinedload(Comment.reposts)  # Eager load reposts for each comment
    ).first()
    
    if post:
        # Filter comments without parent_id
        top_level_comments = [
            comment for comment in post.comments if comment.parent_id is None
        ]
        return {
            "post": post,
            "top_level_comments": top_level_comments,
        }
    else:
        return None

def get_FYP_and_reposts(db: Session):
    return db.query(Post).options(
        joinedload(Post.reposts),
        joinedload(Post.comments)
    ).all()
  


def get_user_posts(db: Session, user_id: str, email: str):
    posts_query = ( db.query(Post).filter(Post.email == email).order_by(Post.date.desc()).options(
        joinedload(Post.comments),
        joinedload(Post.owner),
        joinedload(Post.reposts)
    )
    )
    posts = posts_query.all()
    return {"posts": posts}


def add_like(db: Session, post_id: str, user_id: str):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()

        if not post:
            logger.error("Post not found with id: %s", post_id)
            return None

        current_likes = post.likes or []
        
        if user_id in current_likes:
            logger.info("user id found: %s", user_id)
            current_likes.remove(user_id)
        else:
            logger.info("user id not found: %s", user_id)
            current_likes.append(user_id)

        logger.info("current likes after action: %s", current_likes)

        post.likes = current_likes
        flag_modified(post, "likes")
        db.commit()
        logger.info("Database updated successfully")
        
        db.refresh(post)
        logger.info("Refreshed post likes: %s", post.likes)
        return post
    except Exception as e:
        logger.error("Error in add_like: %s", e)
        raise



def create_post(db: Session, post: PostCreate):
    logger.error("Post contents: %s", post)
    db_post = Post(
        content=post.content,
        user_name=post.user_name,
        email=post.email
    )
    logger.error("db_post: %s", db_post)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post



def update_post(db: Session, post_id: str, post: PostUpdate):
    post_data = post.model_dump(exclude_unset=True)
    db.query(Post).filter(Post.id == post_id).update(post_data)
    db.commit()
    updated_post = db.query(Post).filter(Post.id == post_id).first()
    return updated_post



def delete_post(db: Session, post_id: int):    
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()
    return {"message": "Post deleted"}