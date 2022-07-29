from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# schema/pydantic post model - deasl with request & response of the client

# for base POST model schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# to create post, model schema
class PostCreate(PostBase):
    pass

# user response model schema
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config: # convert it to pydantic model
        orm_mode = True

# send response to client, schema
class ResponsePost(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True

# user create model schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# user login model schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# create token model schema
class Token(BaseModel):
    access_token: str
    token_type: str

# token data schema
class TokenData(BaseModel):
    id: Optional[str] = None
