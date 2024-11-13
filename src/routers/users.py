from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from src.db import SessionLocal
from src.models import models
from src.models.schemas import UserSchema

router = APIRouter(prefix="/api/users")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: int, 
    include: Optional[List[str]] = Query([]), 
    db: Session = Depends(get_db)
):
    query = db.query(models.User).filter(models.User.id == user_id)
    
    if "posts" in include:
        query = query.options(joinedload(models.User.posts))
    if "comments" in include:
        query = query.options(joinedload(models.User.comments))
    
    user = query.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
