from fastapi import FastAPI
from module.auth.auth import router as auth_router
from module.chat.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount the auth router
app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router, prefix="/api")