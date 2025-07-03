from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from models.models import Base, Post
from database import get_db

# Use a test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def setup_function(function):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def teardown_function(function):
    Base.metadata.drop_all(bind=engine)

def test_create_post():
    response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post.", "author": "Test Author"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post."
    assert data["author"] == "Test Author"
    assert "id" in data
    assert "publication_date" in data

def test_read_posts():
    client.post(
        "/api/v1/posts/",
        json={"title": "Test Post 2", "content": "Content 2.", "author": "Author 2"},
    )
    response = client.get("/api/v1/posts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == "Test Post 2"

def test_read_single_post():
    post_data = {"title": "Single Post", "content": "Single content.", "author": "Single Author"}
    create_response = client.post("/api/v1/posts/", json=post_data)
    post_id = create_response.json()["id"]

    response = client.get(f"/api/v1/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Single Post"
    assert data["content"] == "Single content."

def test_read_nonexistent_post():
    response = client.get("/api/v1/posts/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}

def test_update_post():
    post_data = {"title": "Original Title", "content": "Original Content", "author": "Original Author"}
    create_response = client.post("/api/v1/posts/", json=post_data)
    post_id = create_response.json()["id"]

    update_data = {"title": "Updated Title", "content": "Updated Content"}
    response = client.put(f"/api/v1/posts/{post_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated Content"
    assert data["author"] == "Original Author" 

def test_update_nonexistent_post():
    response = client.put(
        "/api/v1/posts/999",
        json={"title": "Nonexistent Update", "content": "Content"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}

def test_delete_post():
    post_data = {"title": "Post to Delete", "content": "Content to delete.", "author": "Author to Delete"}
    create_response = client.post("/api/v1/posts/", json=post_data)
    post_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/posts/{post_id}")
    assert response.status_code == 204 

    get_response = client.get(f"/api/v1/posts/{post_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_post():
    response = client.delete("/api/v1/posts/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}