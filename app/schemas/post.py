from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    post_id:str
    page_id:str
    content: Optional[str] = None
    likes: int =0
    posted_at: Optional[str] = None

