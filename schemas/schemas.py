from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional

class PostBase(SQLModel):
    title: str
    content: str
    author: str

class PostCreate(PostBase):
    pass

class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None

class Post(PostBase):
    id: int
    publication_date: datetime