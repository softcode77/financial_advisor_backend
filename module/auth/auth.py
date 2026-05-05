from fastapi import APIRouter, HTTPException
from migration.schemas import UserCreate, UserLogin
from services.auth import auth

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    success = auth.register_user(user)
    if not success:
        raise HTTPException(status_code=400, detail="Email already registered.")
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    token = auth.authenticate_user(user)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
