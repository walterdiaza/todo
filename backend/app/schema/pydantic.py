from pydantic import BaseModel
from typing import Optional
from datetime import date

class pydantic_user(BaseModel):
    user_name: str
    password: str
    profile_picture: Optional[str]

class pydantic_category(BaseModel):
    name: str
    description: str

class pydantic_create_task(BaseModel):
    description: str
    finish_date: date
    category_id: int

class pydantic_update_task(BaseModel):
    description: Optional[str]
    finish_date: Optional[date]
    status: Optional[str]

class Token(BaseModel):
    access_token: str
    token_type: str

class DataToken(BaseModel):
    id: Optional[str] = None

