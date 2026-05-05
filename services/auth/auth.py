from passlib.hash import bcrypt
from jose import jwt
import os
from migration.database import supabase

SECRET_KEY = os.getenv("JWT_SECRET")

def register_user(user_data):
    # Check if email is already taken
    existing = supabase.table("users").select("*").eq("email", user_data.email).execute()
    if existing.data:
        return None  # Email already in use

    hashed_password = bcrypt.hash(user_data.password)
    data = {
        "email": user_data.email,
        "password": hashed_password
    }
    supabase.table("users").insert(data).execute()
    return True

def authenticate_user(user_data):
    res = supabase.table("users").select("*").eq("email", user_data.email).execute()
    if not res.data:
        return None  # User not found

    db_user = res.data[0]
    if not bcrypt.verify(user_data.password, db_user["password"]):
        return None  # Incorrect password

    # Generate JWT token
    token = jwt.encode({"sub": db_user["email"]}, SECRET_KEY)
    return token
