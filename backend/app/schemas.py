from typing import List, Optional

from pydantic import BaseModel


class Profile(BaseModel):
    name: str
    title: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = []

    class Config:
        orm_mode = True
