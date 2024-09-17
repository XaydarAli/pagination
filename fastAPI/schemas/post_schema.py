from pydantic import BaseModel
from typing import Optional


class PostCreateModel(BaseModel):
    caption: Optional [str]
    image_path: Optional[str]


class PostUpdateModel(BaseModel):
    caption: Optional[str]
    image_path: Optional[str]


