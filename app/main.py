from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

# the root path of the API
@app.get("/")
async def root():
    return {"message": "Welcome to My API!!!"}

