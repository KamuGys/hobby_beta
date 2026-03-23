from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List, Optional

class TagRead(BaseModel):
    id: int
    name: str

class PostCreate(BaseModel):
    title: str
    content: str
    image_url: Optional[HttpUrl] = None
    hobby_done: bool = False
    tag_ids: List[int] = []

class PostRead(BaseModel):
    id: int
    title: str
    content: str
    image_url: Optional[str] = None
    hobby_done: bool
    created_at: datetime
    user_id: int
    user_username: str
    user_photo: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0
    reposts_count: int = 0
    is_liked_by_me: bool = False
    is_reposted_by_me: bool = False
    tags: List[TagRead] = []

    class Config:
        from_attributes = True