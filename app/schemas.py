from datetime import datetime
from pydantic import BaseModel, EmailStr

# schema/pydantic post model - deasl with request & response of the client

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class ResponsePost(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config: # convert it to pydantic model
        orm_mode = True
