"""
Tests for the user-related API endpoints.
"""

from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.db import get_db
from src.models import models

client = TestClient(app)

def test_get_user_with_valid_include(mock_db):
    """Test retrieval of a user with valid include fields: posts and comments."""
    mock_user = models.User(id=1, username="test_user")
    mock_post = models.Post(id=1, title="Post Title", content="Post Content", user_id=1)
    mock_comment = models.Comment(id=1, content="Great post!", user_id=1, post_id=1)
    mock_user.posts = [mock_post]
    mock_user.comments = [mock_comment]

    mock_db.query(models.User).filter(id=1).first.return_value = mock_user
    mock_db.query().filter().options.return_value = mock_db.query().filter()

    response = client.get("/api/users/1?include=posts,comments")

    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == "test_user"
    assert "posts" in user_data
    assert "comments" in user_data
    assert user_data["posts"][0]["title"] == "Post Title"
    assert user_data["comments"][0]["content"] == "Great post!"

def test_get_user_invalid_include():
    """Test retrieval of a user with an invalid include field, expecting a 400 error."""
    response = client.get("/api/users/1?include=invalid_field")

    assert response.status_code == 400
    assert "Invalid fields in include parameter" in response.json()["detail"]

def test_get_user_not_found(mock_db):
    """Test retrieval of a non-existent user, expecting a 404 error."""
    mock_db.query(models.User).filter(id=9999).first.return_value = None

    response = client.get("/api/users/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_user_no_include(mock_db):
    """Test retrieval of a user without including related fields."""
    mock_user = models.User(id=1, username="test_user")
    mock_db.query(models.User).filter(id=1).first.return_value = mock_user

    response = client.get("/api/users/1")

    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == "test_user"
    assert "posts" not in user_data
    assert "comments" not in user_data
