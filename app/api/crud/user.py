from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session, joinedload
from app.api.schemas.users import UserCreate, UserUpdate
from app.models import User, Comment
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def get_users(db: Session) :
    return (
        db.query(User).all()
    )
        

def get_user_with_posts_and_replies(db: Session, user_id: int):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .options(
            joinedload(User.posts),                    
            joinedload(User.comments).joinedload(Comment.replies), 
            joinedload(User.replies)                  
        )
        .first()
    )


def get_user(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    return {"user": user}


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



def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    user_data = user.model_dump(exclude_unset=True)
    db.query(User).filter(User.email == user_id).update(user_data)
    db.commit()
    return user_data



def update_following_and_followers(db: Session, my_id: str, their_id: str):
    # Retrieve both users from the database
    my_user = db.query(User).filter(User.id == my_id).first()
    their_user = db.query(User).filter(User.id == their_id).first()

    # Update following list for the current user
    updated_my_following = my_user.following or []
    if their_id in updated_my_following:
        updated_my_following.remove(their_id)  # Remove their ID if it exists
    else:
        updated_my_following.append(their_id)  # Add their ID if it doesn't exist

    # Update followers list for the target user
    updated_their_followers = their_user.followers or []
    if my_id in updated_their_followers:
        updated_their_followers.remove(my_id)  # Remove my ID if it exists
    else:
        updated_their_followers.append(my_id)  # Add my ID if it doesn't exist


    my_user.following = updated_my_following
    their_user.followers = updated_their_followers

    # Commit changes
    db.commit()
    return {"message": "Followers and following updated successfully"}



def delete_user(user_id: str, db: Session = Depends(get_db)):
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return {"message": "User deleted"}
