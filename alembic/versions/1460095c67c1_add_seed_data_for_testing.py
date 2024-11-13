"""Add seed data for testing

Revision ID: 1460095c67c1
Revises: de2822dbd4ca
Create Date: 2024-11-13 19:22:06.558972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1460095c67c1'
down_revision: Union[str, None] = 'de2822dbd4ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add sample users
    op.execute("INSERT INTO users (id, username) VALUES (1, 'test_user1')")
    op.execute("INSERT INTO users (id, username) VALUES (2, 'test_user2')")
    op.execute("INSERT INTO users (id, username) VALUES (3, 'test_user3')")
    op.execute("INSERT INTO users (id, username) VALUES (4, 'test_user4')")

    # Add sample posts with varying statuses
    op.execute("INSERT INTO posts (id, title, content, status, user_id) VALUES (1, 'Tech Post 1', 'Content about tech 1', 'draft', 1)")
    op.execute("INSERT INTO posts (id, title, content, status, user_id) VALUES (2, 'Life Post', 'Content about life', 'published', 2)")
    op.execute("INSERT INTO posts (id, title, content, status, user_id) VALUES (3, 'Travel Post', 'Content about travel', 'archived', 3)")
    op.execute("INSERT INTO posts (id, title, content, status, user_id) VALUES (4, 'Tech Post 2', 'Content about tech 2', 'draft', 4)")

    # Add sample comments for various posts
    op.execute("INSERT INTO comments (id, content, user_id, post_id) VALUES (1, 'Interesting post!', 1, 1)")
    op.execute("INSERT INTO comments (id, content, user_id, post_id) VALUES (2, 'Great insights!', 2, 1)")
    op.execute("INSERT INTO comments (id, content, user_id, post_id) VALUES (3, 'I love this topic!', 3, 2)")
    op.execute("INSERT INTO comments (id, content, user_id, post_id) VALUES (4, 'Can’t wait to try this!', 4, 3)")
    op.execute("INSERT INTO comments (id, content, user_id, post_id) VALUES (5, 'Very informative.', 1, 4)")

    # Add more tags
    op.execute("INSERT INTO tags (id, name) VALUES (1, 'tech')")
    op.execute("INSERT INTO tags (id, name) VALUES (2, 'life')")
    op.execute("INSERT INTO tags (id, name) VALUES (3, 'travel')")
    op.execute("INSERT INTO tags (id, name) VALUES (4, 'lifestyle')")

    # Associate posts with multiple tags in the post_tags table
    op.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (1, 1)")
    op.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (1, 2)")
    op.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (2, 2)")
    op.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (3, 3)")
    op.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (4, 1)")
    op.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (4, 4)")

def downgrade():
    # Remove seed data in reverse order for rollback
    op.execute("DELETE FROM post_tags WHERE post_id IN (1, 2, 3, 4)")
    op.execute("DELETE FROM tags WHERE id IN (1, 2, 3, 4)")
    op.execute("DELETE FROM comments WHERE id IN (1, 2, 3, 4, 5)")
    op.execute("DELETE FROM posts WHERE id IN (1, 2, 3, 4)")
    op.execute("DELETE FROM users WHERE id IN (1, 2, 3, 4)")
