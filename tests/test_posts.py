import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.models import Post
from app.api.schemas.posts import PostCreate, PostUpdate
from app.main import get_post, add_like, create_post, delete_post

@pytest.fixture
def mock_db():
    """Fixture for a mocked database session."""
    return MagicMock(spec=Session)

def test_get_post(mock_db):
    """Test get_post function."""
    # Arrange
    mock_post = Post(id=1, content="Test post", comments=[], reposts=[])
    mock_db.query().filter().options().first.return_value = mock_post

    # Act
    result = get_post(mock_db, post_id=1)

    # Assert
    assert result["post"] == mock_post
    assert result["top_level_comments"] == []

def test_add_like(mock_db):
    """Test add_like function."""
    # Arrange
    mock_post = Post(id=1, likes=["user1"])
    mock_db.query().filter().first.return_value = mock_post

    # Act: Add a new like
    updated_post = add_like(mock_db, post_id=1, user_id="user2")

    # Assert
    assert "user2" in updated_post.likes
    mock_db.commit.assert_called_once()

    # Act: Remove the like
    updated_post = add_like(mock_db, post_id=1, user_id="user2")
    assert "user2" not in updated_post.likes

def test_create_post(mock_db):
    """Test create_post function."""
    # Arrange
    post_data = PostCreate(content="New post", user_name="user1", email="user1@example.com")
    mock_post = Post(content="New post", user_name="user1", email="user1@example.com")
    mock_db.add.return_value = None
    mock_db.refresh.return_value = mock_post

    # Act
    result = create_post(mock_db, post_data)

    # Assert
    assert result.content == "New post"
    assert result.user_name == "user1"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

def test_delete_post(mock_db):
    """Test delete_post function."""
    # Act
    result = delete_post(mock_db, post_id=1)

    # Assert
    mock_db.query().filter().delete.assert_called_once()
    mock_db.commit.assert_called_once()
    assert result == {"message": "Post deleted"}
