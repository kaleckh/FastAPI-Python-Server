import pytest
from unittest.mock import MagicMock
from app.models import Post, Comment
from app.api.schemas.posts import PostCreate, PostUpdate
from app.api.crud.post import (
    get_posts,
    get_post,
    get_FYP_and_reposts,
    get_user_posts,
    add_like,
    create_post,
    update_post,
    delete_post
)

@pytest.fixture
def mock_db():
    """Fixture to mock the database session."""
    return MagicMock()

def test_get_posts(mock_db):
    """Test get_posts function."""
    # Arrange
    mock_posts = [Post(id="1", content="Test Post 1"), Post(id="2", content="Test Post 2")]
    mock_db.query().all.return_value = mock_posts

    # Act
    result = get_posts(mock_db)

    # Assert
    assert len(result) == 2
    assert result[0].content == "Test Post 1"
    assert result[1].content == "Test Post 2"

def test_get_post(mock_db):
    """Test get_post function."""
    # Arrange
    mock_post = Post(id="1", content="Test Post", comments=[
        Comment(id="1", content="Comment 1", parent_id=None),
        Comment(id="2", content="Comment 2", parent_id="1")
    ])
    mock_db.query().filter().options().first.return_value = mock_post

    # Act
    result = get_post(mock_db, post_id="1")

    # Assert
    assert result["post"].id == "1"
    assert len(result["top_level_comments"]) == 1
    assert result["top_level_comments"][0].content == "Comment 1"

def test_get_FYP_and_reposts(mock_db):
    """Test get_FYP_and_reposts function."""
    # Arrange
    mock_posts = [Post(id="1", content="Test Post 1"), Post(id="2", content="Test Post 2")]
    mock_db.query().options().all.return_value = mock_posts

    # Act
    result = get_FYP_and_reposts(mock_db)

    # Assert
    assert len(result) == 2
    assert result[0].content == "Test Post 1"
    assert result[1].content == "Test Post 2"

def test_get_user_posts(mock_db):
    """Test get_user_posts function."""
    # Arrange
    mock_posts = [Post(id="1", content="User Post 1"), Post(id="2", content="User Post 2")]
    mock_db.query().filter().order_by().options().all.return_value = mock_posts

    # Act
    result = get_user_posts(mock_db, user_id="user1", email="user@example.com")

    # Assert
    assert len(result["posts"]) == 2
    assert result["posts"][0].content == "User Post 1"
    assert result["posts"][1].content == "User Post 2"

def test_add_like(mock_db):
    """Test add_like function."""
    # Arrange
    mock_post = Post(id="1", likes=["user1"])
    mock_db.query().filter().first.return_value = mock_post

    # Act: Add a new like
    updated_post = add_like(mock_db, post_id="1", user_id="user2")

    # Assert
    assert "user2" in updated_post.likes
    mock_db.commit.assert_called_once()

    # Act: Remove the like
    updated_post = add_like(mock_db, post_id="1", user_id="user2")
    assert "user2" not in updated_post.likes

def test_create_post(mock_db):
    """Test create_post function."""
    # Arrange
    post_data = PostCreate(content="New post", user_name="user1", email="user@example.com")
    mock_post = Post(id="1", content="New post", user_name="user1", email="user@example.com")
    mock_db.add.return_value = None
    mock_db.refresh.return_value = mock_post

    # Act
    result = create_post(mock_db, post_data)

    # Assert
    assert result.content == "New post"
    assert result.user_name == "user1"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

def test_update_post(mock_db):
    """Test update_post function."""
    # Arrange
    post_id = "1"
    post_update_data = PostUpdate(content="Updated post")
    mock_updated_post = Post(id=post_id, content="Updated post")

    mock_db.query().filter().update.return_value = None
    mock_db.query().filter().first.return_value = mock_updated_post

    # Act
    result = update_post(mock_db, post_id, post_update_data)

    # Assert
    assert result.content == "Updated post"
    mock_db.commit.assert_called_once()

def test_delete_post(mock_db):
    """Test delete_post function."""
    # Arrange
    mock_db.query().filter().delete.return_value = 1

    # Act
    result = delete_post(mock_db, post_id=1)

    # Assert
    assert result == {"message": "Post deleted"}
    mock_db.commit.assert_called_once()
