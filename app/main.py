from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# the root path of the API
@app.get("/")
async def root():
    return {"message": "Welcome to My API!!!"}

