from fastapi import APIRouter, Depends, HTTPException, Header
from migration.schemas import ChatThreadCreate, ChatMessageCreate
from jose import jwt
import os
from services.chat import chat

router = APIRouter()
SECRET_KEY = os.getenv("JWT_SECRET")

def get_current_user(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY)
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/threads")
def create_thread(thread: ChatThreadCreate, user_email: str = Depends(get_current_user)):
    thread_id = chat.create_thread_service(thread, user_email)
    return {"message": "Thread created", "thread_id": thread_id}

@router.post("/chat/{thread_id}")
def add_chat_message(thread_id: str, chat: ChatMessageCreate, user_email: str = Depends(get_current_user)):
    chat.add_user_message(thread_id, chat.message)
    llm_response = chat.handle_llm_response(thread_id)
    chat.add_llm_response(thread_id, llm_response)
    return {"response": llm_response}

@router.get("/threads")
def get_threads(user_email: str = Depends(get_current_user)):
    return chat.get_threads_service(user_email)

@router.get("/chat/{thread_id}")
def get_chat(thread_id: str, user_email: str = Depends(get_current_user)):
    data = chat.get_chat_history(thread_id, user_email)
    if data is None:
        raise HTTPException(status_code=403, detail="Thread not found or unauthorized")
    return data
