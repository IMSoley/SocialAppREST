from pydantic import BaseModel

# schema/pydantic post model - deasl with request & response of the client

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

