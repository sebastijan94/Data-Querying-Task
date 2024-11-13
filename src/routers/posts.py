from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from src.db import SessionLocal
from src.models import models
from src.models.schemas import PostSchema

router = APIRouter(prefix="/api/posts")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[PostSchema])
def get_posts(
    status: Optional[str] = Query(None), 
    include: Optional[List[str]] = Query([]), 
    db: Session = Depends(get_db)
):
    query = db.query(models.Post)
    
    if status:
        query = query.filter(models.Post.status == status)
    
    if "tags" in include:
        query = query.options(joinedload(models.Post.tags))
    if "user" in include:
        query = query.options(joinedload(models.Post.user))
    if "comments" in include:
        query = query.options(joinedload(models.Post.comments))
    
    return query.all()

@router.get("/{post_id}", response_model=PostSchema)
def get_post(
    post_id: int, 
    include: Optional[List[str]] = Query([]), 
    db: Session = Depends(get_db)
):
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
    return post
