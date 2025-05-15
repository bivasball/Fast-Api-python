from fastapi import FastAPI
from .routers import post,auth


app = FastAPI()

app.include_router(post.router)
app.include_router(auth.router)