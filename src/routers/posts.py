"""
Post-related API endpoints.
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from src.db import get_db
from src.models import models
from src.models.schemas import PostSchema
from src.utils.validators import validate_include_param
from src.utils.constants import ALLOWED_INCLUDES_POSTS, RELATIONSHIP_LOADERS

router = APIRouter(prefix="/api/posts")

@router.get("/")
def get_posts(
    status: Optional[str] = Query(None, pattern="^(published|draft|archived)$"),
    include: Optional[str] = Query(""), 
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of posts with optional filters and related data.

    Parameters:
        status (Optional[str]): Filter posts by status (e.g., "published", "draft", "archived").
        include (Optional[str]): Comma-separated list of related data to include (e.g., "tags,user,comments").
        db (Session): Database session dependency.

    Returns:
        List[dict]: List of posts with specified filters and relationships included.
    """
    include = [item.strip() for item in include.split(",")] if include else []
    validate_include_param(include, ALLOWED_INCLUDES_POSTS)

    query = db.query(models.Post)
    
    if status:
        query = query.filter(models.Post.status == status)
    
    for field in include:
        if field in RELATIONSHIP_LOADERS:
            query = query.options(joinedload(RELATIONSHIP_LOADERS[field]))
    
    posts = query.all()
    return [PostSchema.model_validate(post).model_dump(exclude_defaults=True) for post in posts]

@router.get("/{post_id}")
def get_post(
    post_id: int, 
    include: Optional[str] = Query(""), 
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific post by ID, optionally including related data.

    Parameters:
        post_id (int): The unique ID of the post to retrieve.
        include (Optional[str]): Comma-separated list of related data to include (e.g., "tags,user,comments").
        db (Session): Database session dependency.

    Returns:
        dict: The post details with specified relationships included.
    """
    include = [item.strip() for item in include.split(",")] if include else []
    validate_include_param(include, ALLOWED_INCLUDES_POSTS)

    query = db.query(models.Post).filter(models.Post.id == post_id)
    
    for field in include:
        if field in RELATIONSHIP_LOADERS:
            query = query.options(joinedload(RELATIONSHIP_LOADERS[field]))
    
    post = query.first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return PostSchema.model_validate(post).model_dump(exclude_defaults=True)
