from fastapi import APIRouter, Depends, HTTPException, Header
from migration.schemas import ChatThreadCreate, ChatMessageCreate
from jose import jwt, JWTError
import os
# from services.chat import chat
from services.chat import chat as chat_service
from fastapi.responses import StreamingResponse
import json
from uuid import UUID

router = APIRouter()
SECRET_KEY = os.getenv("JWT_SECRET")


# User authentication dependency
def get_current_user(authorization: str = Header(...)):
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")

        token = authorization.split(" ")[1]  # extract the JWT from "Bearer <token>"
        payload = jwt.decode(token, SECRET_KEY)
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


# Thread endpoints
@router.post("/threads")
def create_thread(thread: ChatThreadCreate, user_email: str = Depends(get_current_user)):
    thread_id = chat_service.create_thread_service(thread, user_email)
    return {"message": "Thread created", "thread_id": thread_id}



@router.get("/threads")
def get_threads(user_email: str = Depends(get_current_user)):
    return chat_service.get_threads_service(user_email)


@router.put("/threads/{thread_id}/soft-delete")
def soft_delete_thread(thread_id: str):
    chat_service.get_soft_delete_service(thread_id)
    return {"message": f"Thread {thread_id} successfully soft deleted"}


# Chat endpoints
@router.get("/chat/{thread_id}")
def get_chat(thread_id: str, user_email: str = Depends(get_current_user)):
    data = chat_service.get_chat_history(thread_id, user_email)
    if data is None:
        raise HTTPException(status_code=403, detail="Thread not found or unauthorized")
    return data

@router.post("/chat/{thread_id}")
def add_chat_message(thread_id: str, chat: ChatMessageCreate, user_email: str = Depends(get_current_user)):    
    chat_service.add_user_message(thread_id, chat.message)
    def generate_response():
        complete_response = ""
        for chunk in chat_service.handle_llm_response(thread_id):
            complete_response += chunk
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        chat_service.add_llm_response(thread_id, complete_response)
    
    return StreamingResponse(generate_response(), media_type="text/plain")

