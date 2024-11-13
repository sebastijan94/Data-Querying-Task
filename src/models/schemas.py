from pydantic import BaseModel
from typing import List, Optional

class TagSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CommentSchema(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    id: int
    username: str
    posts: Optional[List['PostSchema']] = []
    comments: Optional[List[CommentSchema]] = []

    class Config:
        from_attributes = True

class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    user: Optional[UserSchema] = None
    tags: Optional[List[TagSchema]] = []
    comments: Optional[List[CommentSchema]] = []

    class Config:
        from_attributes = True

UserSchema.model_rebuild()
PostSchema.model_rebuild()
