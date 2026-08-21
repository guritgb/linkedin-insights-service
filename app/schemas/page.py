from pydantic import BaseModel , Field
from typing import Optional

class Page(BaseModel):
    page_id:str
    linkedin_id:Optional[str] = None
    name:str
    url:str
    profile_pic: Optional[str] = None
    description: Optional[str] = None
    website : Optional[str] = None
    industry: Optional[str] = None
    followers: Optional[int] = None
    headcount: Optional[str] = None
    specialities: list[str] = Field(default_factory=list)

