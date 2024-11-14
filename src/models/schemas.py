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

class UserSummarySchema(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class PostSummarySchema(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    id: int
    username: str
    posts: Optional[List[PostSummarySchema]] = []
    comments: Optional[List[CommentSchema]] = []

    class Config:
        from_attributes = True

class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    status: str
    user: Optional[UserSummarySchema] = None
    tags: Optional[List[TagSchema]] = []
    comments: Optional[List[CommentSchema]] = []

    class Config:
        from_attributes = True
