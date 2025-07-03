from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/blogdb")

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-csearch_path=blogs"},
    echo=True  
)

def get_session():
    with Session(engine) as session:
        yield session