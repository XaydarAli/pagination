from pydantic import BaseModel
from typing import Optional


class CommentCreateModel(BaseModel):
    user_id: Optional[int]
    post_id: Optional[int]
    content: Optional[str]


class CommentUpdateModel(BaseModel):
    user_id: Optional[int]
    post_id: Optional[int]
    content: Optional[str]
