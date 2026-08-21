from pydantic import BaseModel
from typing import Optional

class Person(BaseModel):
    person_id:str
    page_id:str
    name: Optional[str] = None
    profile_url: Optional[str] = None
    

