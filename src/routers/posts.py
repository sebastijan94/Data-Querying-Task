from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from src.db import get_db
from src.models import models
from src.models.schemas import PostSchema
from src.utils.validators import validate_include_param
from src.utils.constants import ALLOWED_INCLUDES_POSTS

router = APIRouter(prefix="/api/posts")

@router.get("/")
def get_posts(
    status: Optional[str] = Query(None, pattern="^(published|draft|archived)$"),
    include: Optional[str] = Query(""), 
    db: Session = Depends(get_db)
):
    include = [item.strip() for item in include.split(",")] if include else []
    validate_include_param(include, ALLOWED_INCLUDES_POSTS)

    query = db.query(models.Post)
    
    if status:
        query = query.filter(models.Post.status == status)
    
    if "tags" in include:
        query = query.options(joinedload(models.Post.tags))
    if "user" in include:
        query = query.options(joinedload(models.Post.user))
    if "comments" in include:
        query = query.options(joinedload(models.Post.comments))
    
    posts = query.all()
    
    return [PostSchema.model_validate(post).model_dump(exclude_defaults=True) for post in posts]

@router.get("/{post_id}")
def get_post(
    post_id: int, 
    include: Optional[str] = Query(""), 
    db: Session = Depends(get_db)
):
    include = [item.strip() for item in include.split(",")] if include else []
    validate_include_param(include, ALLOWED_INCLUDES_POSTS)

    query = db.query(models.Post).filter(models.Post.id == post_id)
    
    if "tags" in include:
        query = query.options(joinedload(models.Post.tags))
    if "user" in include:
        query = query.options(joinedload(models.Post.user))
    if "comments" in include:
        query = query.options(joinedload(models.Post.comments))
    
    post = query.first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return PostSchema.model_validate(post).model_dump(exclude_defaults=True)
