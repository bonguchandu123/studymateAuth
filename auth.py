from fastapi import APIRouter, HTTPException
from schemas import UserCreate, UserLogin
from database import users_collection
from utils import hash_password, verify_password, create_token


auth_router = APIRouter()

@auth_router.post("/signup")
def signup(user: UserCreate):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password)
    }
    users_collection.insert_one(user_dict)

    token = create_token({"email": user.email})
    return {"token": token, "username": user.username}

@auth_router.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"email": user.email})
    return {"token": token, "username": db_user["username"]}
