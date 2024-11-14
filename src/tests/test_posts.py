from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.db import get_db
from src.models import models

client = TestClient(app)

def test_get_post_no_include(mock_db):
    mock_db.query(models.Post).filter(id=1).first.return_value = models.Post(
        id=1, title="Post 1", content="Content 1", status="draft", user_id=1
    )

    response = client.get("/api/posts/1")

    assert response.status_code == 200
    data = response.json()
    assert "tags" not in data
    assert "user" not in data
    assert "comments" not in data

def test_get_post_with_include_user(mock_db):
    mock_user = models.User(id=1, username="test_user")
    mock_db.query(models.Post).filter(id=1).first.return_value = models.Post(
        id=1, title="Post 1", content="Content 1", status="draft", user_id=1, user=mock_user
    )
    mock_db.query().filter().options.return_value = mock_db.query().filter()

    response = client.get("/api/posts/1?include=user")

    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert data["user"]["username"] == "test_user"

def test_get_post_with_include_tags(mock_db):
    mock_tag = models.Tag(id=1, name="Sample Tag")
    mock_db.query(models.Post).filter(id=1).first.return_value = models.Post(
        id=1, title="Post 1", content="Content 1", status="draft", user_id=1, tags=[mock_tag]
    )
    mock_db.query().filter().options.return_value = mock_db.query().filter()

    response = client.get("/api/posts/1?include=tags")

    assert response.status_code == 200
    data = response.json()
    assert "tags" in data
    assert data["tags"][0]["name"] == "Sample Tag"

def test_get_post_with_include_comments(mock_db):
    mock_comment = models.Comment(id=1, content="Great post!", user_id=1, post_id=1)
    mock_db.query(models.Post).filter(id=1).first.return_value = models.Post(
        id=1, title="Post 1", content="Content 1", status="draft", user_id=1, comments=[mock_comment]
    )
    mock_db.query().filter().options.return_value = mock_db.query().filter()

    response = client.get("/api/posts/1?include=comments")

    assert response.status_code == 200
    data = response.json()
    assert "comments" in data
    assert data["comments"][0]["content"] == "Great post!"

def test_get_post_with_include_all(mock_db):
    mock_user = models.User(id=1, username="test_user")
    mock_tag = models.Tag(id=1, name="Sample Tag")
    mock_comment = models.Comment(id=1, content="Great post!", user_id=1, post_id=1)
    mock_db.query(models.Post).filter(id=1).first.return_value = models.Post(
        id=1, title="Post 1", content="Content 1", status="draft", user_id=1,
        user=mock_user, tags=[mock_tag], comments=[mock_comment]
    )
    mock_db.query().filter().options.return_value = mock_db.query().filter()

    response = client.get("/api/posts/1?include=user&include=tags&include=comments")

    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert "tags" in data
    assert "comments" in data
    assert data["user"]["username"] == "test_user"
    assert data["tags"][0]["name"] == "Sample Tag"
    assert data["comments"][0]["content"] == "Great post!"

def test_get_posts_no_include(mock_db):
    mock_db.query(models.Post).all.return_value = [
        models.Post(id=1, title="Post 1", content="Content 1", status="draft", user_id=1),
        models.Post(id=2, title="Post 2", content="Content 2", status="published", user_id=2)
    ]

    response = client.get("/api/posts")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Post 1"
    assert "tags" not in data[0] 
    assert "user" not in data[0]

def test_get_posts_with_include(mock_db):
    mock_user = models.User(id=1, username="test_user")
    mock_tag = models.Tag(id=1, name="Sample Tag")
    mock_db.query(models.Post).all.return_value = [
        models.Post(
            id=1,
            title="Post 1",
            content="Content 1",
            status="draft",
            user_id=1,
            user=mock_user,
            tags=[mock_tag]
        ),
        models.Post(
            id=2,
            title="Post 2",
            content="Content 2",
            status="published",
            user_id=2,
            user=mock_user,
            tags=[mock_tag]
        )
    ]
    mock_db.query().options.return_value = mock_db.query()

    response = client.get("/api/posts?include=tags&include=user")

    assert response.status_code == 200
    data = response.json()
    assert "tags" in data[0]
    assert "user" in data[0]
