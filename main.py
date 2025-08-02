from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import auth_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8501",
    "http://127.0.0.1:8501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

