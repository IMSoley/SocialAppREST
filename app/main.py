from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# for post model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# hardcoded posts
my_posts = [
    {"title": "My first post", "content": "This is my first post", "id": 1},
    {"title": "My second post", "content": "This is my second post", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

def find_index(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i
    return None

# the root path of the API
@app.get("/")
async def root():
    return {"message": "Welcome to My API!!!"}

# get all posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(1, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# get a specific post by id
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": post}

# delete a specific post by id
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update a specific post by id
@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    index = find_index(post_id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post = post.dict()
    post["id"] = post_id
    my_posts[index] = post
    return {"data": post}

