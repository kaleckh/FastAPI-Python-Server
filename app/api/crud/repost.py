from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.api.schemas.repost import RepostCreate, RepostUpdate, RepostDelete
from app.models import Repost
from sqlalchemy import and_
from fastapi import FastAPI, Depends
import logging

logger = logging.getLogger(__name__)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def create_repost(db: Session, repost: RepostCreate): 
    logger.debug("stuff: %s", repost)   
    if repost.post_id:
        delete_count_post = db.query(Repost).filter(
            Repost.post_id == repost.post_id,
            Repost.user_id == repost.user_id
        ).delete()
        logger.debug(
            "Deleted %d repost(s) with post_id=%s and user_id=%s",
            delete_count_post, repost.post_id, repost.user_id
        )
        
    if repost.comment_id:
        delete_count_comment = db.query(Repost).filter(
            Repost.comment_id == repost.comment_id,
            Repost.user_id == repost.user_id
        ).delete()
        logger.debug(
            "Deleted %d repost(s) with comment_id=%s and user_id=%s",
            delete_count_comment, repost.comment_id, repost.user_id
        )
    db_repost = Repost(
        post_id=repost.post_id if repost.post_id else None,
        comment_id=repost.comment_id if repost.comment_id else None,
        user_id=repost.user_id,
    )
    db.add(db_repost)
    logger.debug("Added new repost: %s", db_repost)

    db.commit()
    logger.debug("Committed transaction")

    db.refresh(db_repost)
    logger.debug("Refreshed repost: %s", db_repost)

    return db_repost


def delete_repost(db: Session, req: RepostDelete):
    logger.debug("Refreshed repost: %s", req.comment_id)
    if req.comment_id:
        delete_count = db.query(Repost).filter(
            and_(
                Repost.user_id == req.user_id,
                Repost.comment_id == req.comment_id
            )
        ).delete()
        db.commit()
        return {"message": f"Deleted {delete_count} repost(s) with comment_id={req.comment_id}"}
    
    if req.post_id:
        delete_count = db.query(Repost).filter(
            and_(
                Repost.user_id == req.user_id,
                Repost.post_id == req.post_id
            )
        ).delete()
        db.commit()
        return {"message": f"Deleted {delete_count} repost(s) with post_id={req.post_id}"}
    return {"message": "No repost was deleted; neither comment_id nor post_id was provided."}
