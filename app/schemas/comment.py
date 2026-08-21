from pydantic import BaseModel

class Comment(BaseModel):
    comment_id:str
    post_id:str
    author:str
    content:str
    posted_at:str
    likes:int=0


