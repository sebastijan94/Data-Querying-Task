"""
This module defines constants
"""

from src.models import models

# Allowed fields for the `include` parameter in posts and users
ALLOWED_INCLUDES_POSTS = {"tags", "user", "comments"}
ALLOWED_INCLUDES_USERS = {"posts", "comments"}

# Mapping of include fields to SQLAlchemy relationship attributes
RELATIONSHIP_LOADERS = {
    "User": {
        "posts": models.User.posts,
        "comments": models.User.comments,
    },
    "Post": {
        "tags": models.Post.tags,
        "user": models.Post.user,
        "comments": models.Post.comments,
    },
}
