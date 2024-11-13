from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from src.db import get_db
from src.models import models
from src.models.schemas import UserSchema
from src.utils.validators import validate_include_param

router = APIRouter(prefix="/api/users")

@router.get("/{user_id}")
def get_user(
    user_id: int, 
    include: Optional[List[str]] = Query([]), 
    db: Session = Depends(get_db)
):
    validate_include_param(include)

    query = db.query(models.User).filter(models.User.id == user_id)
    
    if "posts" in include:
        query = query.options(joinedload(models.User.posts))
    if "comments" in include:
        query = query.options(joinedload(models.User.comments))
    
    user = query.first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserSchema.model_validate(user).model_dump(exclude_defaults=True)
