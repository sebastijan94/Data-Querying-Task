"""
This module defines the SQLAlchemy models representing database tables for the application,
including users, posts, comments, and tags, as well as their relationships.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.base import Base

# Association table for post-tag many-to-many relationship
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)

    posts = relationship("Post", back_populates="user", lazy="noload")
    comments = relationship("Comment", back_populates="user", lazy="noload")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    status = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="posts", lazy="noload")
    comments = relationship("Comment", back_populates="post", lazy="noload")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts", lazy="noload")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    user = relationship("User", back_populates="comments", lazy="noload")
    post = relationship("Post", back_populates="comments", lazy="noload")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    posts = relationship("Post", secondary=post_tags, back_populates="tags", lazy="noload")
