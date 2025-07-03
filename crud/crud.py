from sqlmodel import Session, select
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

from models import models
from schemas import schemas

def get_post(session: Session, post_id: int):
    return session.get(models.Post, post_id)

def get_posts(session: Session, skip: int = 0, limit: int = 100) -> List[models.Post]:
    statement = select(models.Post).offset(skip).limit(limit)
    return session.exec(statement).all()

def create_post(session: Session, post: schemas.PostCreate):
    logger.info(f"Attempting to create post: {post.title}")
    try:
        db_post = models.Post.from_orm(post)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        logger.info(f"Post created successfully with ID: {db_post.id}")
        return db_post
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating post: {e}", exc_info=True)
        raise

def update_post(session: Session, post_id: int, post: schemas.PostUpdate):
    logger.info(f"Attempting to update post ID: {post_id} with data: {post.dict(exclude_unset=True)}")
    db_post = session.get(models.Post, post_id)
    if db_post:
        try:
            post_data = post.dict(exclude_unset=True)
            for key, value in post_data.items():
                setattr(db_post, key, value)
            session.add(db_post)
            session.commit()
            session.refresh(db_post)
            logger.info(f"Post ID: {post_id} updated successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating post ID: {post_id}: {e}", exc_info=True)
            raise
    else:
        logger.warning(f"Post with ID: {post_id} not found for update.")
    return db_post

def delete_post(session: Session, post_id: int):
    logger.info(f"Attempting to delete post ID: {post_id}")
    db_post = session.get(models.Post, post_id)
    if db_post:
        try:
            session.delete(db_post)
            session.commit()
            logger.info(f"Post ID: {post_id} deleted successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting post ID: {post_id}: {e}", exc_info=True)
            raise
    else:
        logger.warning(f"Post with ID: {post_id} not found for deletion.")
    return db_post