import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.models import Base, Post


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create tables in the test database
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_test_data():
    """Setup test data before each test."""
    db = TestingSessionLocal()
    test_post = Post(content="Test post", user_name="testuser", email="testuser@example.com")
    db.add(test_post)
    db.commit()
    db.refresh(test_post)
    yield db  
    db.close()
    Base.metadata.drop_all(bind=engine) 

def test_get_post(setup_test_data):
    """Test fetching a post by ID."""
    response = client.get("/posts/1")
    assert response.status_code == 200
    assert response.json()["post"]["content"] == "Test post"

def test_create_post():
    """Test creating a new post."""
    payload = {"content": "New test post", "user_name": "newuser", "email": "newuser@example.com"}
    response = client.post("/posts/", json=payload)
    assert response.status_code == 201
    assert response.json()["content"] == "New test post"

def test_add_like(setup_test_data):
    """Test liking a post."""
    response = client.post("/posts/1/like", json={"user_id": "user1"})
    assert response.status_code == 200
    assert "user1" in response.json()["likes"]

    # Test unliking the same post
    response = client.post("/posts/1/like", json={"user_id": "user1"})
    assert response.status_code == 200
    assert "user1" not in response.json()["likes"]

def test_delete_post(setup_test_data):
    """Test deleting a post."""
    response = client.delete("/posts/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Post deleted"}

    # Ensure the post no longer exists
    response = client.get("/posts/1")
    assert response.status_code == 404
