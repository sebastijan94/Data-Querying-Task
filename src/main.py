from typing import List, Optional
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from src.db import SessionLocal
from src.models import models
from src.models.schemas import PostSchema, UserSchema

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/posts", response_model=List[PostSchema])
def get_posts(status: Optional[str] = Query(None), include: Optional[List[str]] = Query([]), db: Session = Depends(get_db)):
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

@app.get("/api/posts/{post_id}", response_model=PostSchema)
def get_post(post_id: int, include: Optional[List[str]] = Query([]), db: Session = Depends(get_db)):
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

@app.get("/api/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int, include: Optional[List[str]] = Query([]), db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == user_id)
    
    if "posts" in include:
        query = query.options(joinedload(models.User.posts))
    if "comments" in include:
        query = query.options(joinedload(models.User.comments))
    
    user = query.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
