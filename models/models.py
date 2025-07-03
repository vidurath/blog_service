from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class Post(SQLModel, table=True):
    __table_args__ = {'schema': 'blogs'}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str
    author: str
    publication_date: datetime = Field(default_factory=datetime.utcnow)