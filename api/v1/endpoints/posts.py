from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from crud import crud
from schemas import schemas
from database import get_session

router = APIRouter()

@router.post("/posts/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_blog_post(post: schemas.PostCreate, session: Session = Depends(get_session)):
    return crud.create_post(session=session, post=post)

@router.get("/posts/", response_model=List[schemas.Post])
def read_blog_posts(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    posts = crud.get_posts(session, skip=skip, limit=limit)
    return posts

@router.get("/posts/{post_id}", response_model=schemas.Post)
def read_blog_post(post_id: int, session: Session = Depends(get_session)):
    db_post = crud.get_post(session, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return db_post

@router.put("/posts/{post_id}", response_model=schemas.Post)
def update_blog_post(post_id: int, post: schemas.PostUpdate, session: Session = Depends(get_session)):
    db_post = crud.update_post(session, post_id=post_id, post=post)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return db_post

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_post(post_id: int, session: Session = Depends(get_session)):
    db_post = crud.delete_post(session, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"message": "Post deleted successfully"}