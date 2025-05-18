from fastapi import FastAPI
from .routers import post, auth, user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:3000",  # Your React app's origin
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS", "GET", "PUT", "DELETE", "HEAD"],
    allow_headers=["*"],  # Or specify the headers you need
)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(user.router)
