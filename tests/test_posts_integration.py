import pytest
import logging
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.models import Post
from app.database import Base

# SQLite test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


# Setup database
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def setup_test_data():
    db = TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)  # Clear old schema
    Base.metadata.create_all(bind=engine)  # Recreate schema

    test_post = Post(content="Test post", username="testuser", email="testuser@example.com")
    db.add(test_post)
    db.commit()
    db.refresh(test_post)
    print("Inserted Post:", test_post.id, test_post.content, test_post.username)
    yield db
    db.rollback()
    db.close()

client = TestClient(app)

def test_get_posts(setup_test_data):  
    db = TestingSessionLocal()
    posts = db.query(Post).all()
    db.close()
    response = client.get("/posts/getPosts")
    assert response.status_code == 200
    assert len(response.json()["Posts"]) > 0


# def test_get_post(setup_test_data):
#     response = client.get("/posts/post", params={"post_id": "1"})
#     assert response.status_code == 200
#     assert response.json()["post"]["content"] == "Test post"

# def test_create_post():
#     payload = {
#         "content": "New test post",
#         "userName": "newuser",
#         "email": "newuser@example.com"
#     }
#     response = client.post("/posts/create", json=payload)
#     assert response.status_code == 200
#     assert response.json()["post"]["content"] == "New test post"

# def test_add_like(setup_test_data):
#     payload = {"postId": "1", "userId": "user1"}
#     response = client.post("/posts/likes", json=payload)
#     assert response.status_code == 200
#     assert "user1" in response.json()["post"]["likes"]

#     response = client.post("/posts/likes", json=payload)
#     assert response.status_code == 200
#     assert "user1" not in response.json()["post"]["likes"]


# def test_update_post(setup_test_data):
#     payload = {"content": "Updated post content"}
#     response = client.put("/posts/update/1", json=payload)
#     assert response.status_code == 200
#     assert response.json()["post"]["content"] == "Updated post content"


# def test_delete_post(setup_test_data):
#     payload = {"post_id": "1"}
#     response = client.post("/posts/delete", json=payload)
#     assert response.status_code == 200
#     assert response.json() == {"message": "Post deleted successfully"}

#     response = client.get("/posts/post", params={"post_id": "1"})
#     assert response.status_code == 404
