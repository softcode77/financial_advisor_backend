from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ChatThreadCreate(BaseModel):
    title: str

class ChatThreadOut(BaseModel):
    id: UUID
    title: str
    created_at: str

class ChatMessageCreate(BaseModel):
    message: str

class ChatMessageOut(BaseModel):
    sender: str  # 'user' or 'llm'
    message: str
    timestamp: str