from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session, joinedload
from app.api.schemas.posts import PostCreate, PostUpdate
from app.models import Post, Repost, User
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



def get_post(db: Session, post_id: str):
    return db.query(Post).filter(Post.id == post_id).options(
        joinedload(Post.comments),
        joinedload(Post.reposts),
    ).first()


def get_FYP_and_reposts(db: Session, user_id: str = None):
    # Fetch posts and reposts based on whether user_id is provided
    if not user_id:
        # Get all posts
        posts = (
            db.query(Post)
            .order_by(Post.date.desc())
            .options(
                joinedload(Post.comments),
                joinedload(Post.owner),
                joinedload(Post.reposts)
            )
            .all()
        )

        # Get all reposts
        reposts = (
            db.query(Repost)
            .order_by(Repost.date.desc())
            .options(
                joinedload(Repost.user),
                joinedload(Repost.post).joinedload(Post.comments),
                joinedload(Repost.post).joinedload(Post.owner),
                joinedload(Repost.post).joinedload(Post.reposts)
            )
            .all()
        )
    else:
        # Verify that the user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User does not exist")

        # Get posts for the user and those they follow
        posts = (
            db.query(Post)
            .filter(Post.owner_id.in_([*user.following, user_id]))  # Owner ID in following list or user_id
            .order_by(Post.date.desc())
            .options(
                joinedload(Post.comments),
                joinedload(Post.owner),
                joinedload(Post.reposts)
            )
            .all()
        )

        # Get reposts for the user and those they follow
        reposts = (
            db.query(Repost)
            .filter(Repost.user_id.in_([*user.following, user_id]))  # User ID in following list or user_id
            .order_by(Repost.date.desc())
            .options(
                joinedload(Repost.user),
                joinedload(Repost.post).joinedload(Post.comments),
                joinedload(Repost.post).joinedload(Post.owner),
                joinedload(Repost.post).joinedload(Post.reposts)
            )
            .all()
        )

    # Combine and sort by date
    query = sorted(
        [*posts, *reposts],
        key=lambda x: x.date,
        reverse=True
    )

    return query




def get_user_posts(db: Session, user_id: str, email: str):

    posts_query = ( db.query(Post).filter(Post.email == email).order_by(Post.date.desc()).options(
        joinedload(Post.comments),
        joinedload(Post.owner),
        joinedload(Post.reposts).joinedload(Repost.post).joinedload(Post.comments),
        joinedload(Post.reposts).joinedload(Repost.user)
    )
    )
    posts = posts_query.all()
    reposts_query = db.query(Repost).filter(Repost.user_id == user_id).order_by(Repost.date.desc()).options(
        joinedload(Repost.post)
    )
    reposts = reposts_query.all()
    return {"posts": posts, "reposts": reposts}


def create_post(db: Session, post: PostCreate):
    db_post = Post(
        content=post.content,
        user_name=post.user_name,
        email=post.email        
    )
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