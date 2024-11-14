from src.models import models

ALLOWED_INCLUDES_POSTS = {"tags", "user", "comments"}
ALLOWED_INCLUDES_USERS = {"posts", "comments"}
RELATIONSHIP_LOADERS = {
    "tags": models.Post.tags,
    "user": models.Post.user,
    "comments": models.Post.comments,
    "posts": models.User.posts,
}