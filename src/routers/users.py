from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from src.db import get_db
from src.models import models
from src.models.schemas import UserSchema
from src.utils.validators import validate_include_param
from src.utils.constants import ALLOWED_INCLUDES_USERS

router = APIRouter(prefix="/api/users")

@router.get("/{user_id}")
def get_user(
    user_id: int, 
    include: Optional[str] = Query(""), 
    db: Session = Depends(get_db)
):
    include = [item.strip() for item in include.split(",")] if include else []
    validate_include_param(include, ALLOWED_INCLUDES_USERS)

    query = db.query(models.User).filter(models.User.id == user_id)
    
    if "posts" in include:
        query = query.options(joinedload(models.User.posts))
    if "comments" in include:
        query = query.options(joinedload(models.User.comments))
    
    user = query.first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserSchema.model_validate(user).model_dump(exclude_defaults=True)
