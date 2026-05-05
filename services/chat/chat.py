from uuid import uuid4
from migration.database import supabase
from agent import _agent


# THREAD SERVICES
def create_thread_service(thread_data, user_email):
    data = {
        "id": str(uuid4()),
        "user_email": user_email,
        "title": thread_data.title,
        "is_deleted": False
    }
    supabase.table("chat_threads").insert(data).execute()
    return data["id"]



def get_threads_service(user_email):
    res = supabase.table("chat_threads")\
        .select("*")\
        .eq("user_email", user_email)\
        .eq("is_deleted", False)\
        .order("created_at", desc=True)\
        .execute()
    return res.data



def get_soft_delete_service(thread_id: str):
    supabase.table("chat_threads")\
        .update({"is_deleted": True})\
        .eq("id", thread_id).execute()


# USER SERVICES

def add_user_message(thread_id, message):
    user_msg = {
        "id": str(uuid4()),
        "thread_id": thread_id,
        "sender": "user",
        "message": message
    }
    supabase.table("chat_messages").insert(user_msg).execute()



def get_message_history(thread_id):
    past_msgs = supabase.table("chat_messages")\
        .select("sender", "message")\
        .eq("thread_id", thread_id)\
        .order("timestamp")\
        .execute()
    return [{"sender": m["sender"], "message": m["message"]} for m in past_msgs.data]


# CHAT AND THREAD SERVICES

def get_chat_history(thread_id, user_email):
    res = supabase.table("chat_threads")\
        .select("id")\
        .eq("id", thread_id)\
        .eq("user_email", user_email)\
        .execute()
    if not res.data:
        return None

    # Fetch messages for the thread
    messages_res = supabase.table("chat_messages")\
        .select("sender, message, timestamp")\
        .eq("thread_id", thread_id)\
        .order("timestamp", desc=False)\
        .execute()
    
    return messages_res.data


# LLM SERVICES

def add_llm_response(thread_id, response):
    llm_msg = {
        "id": str(uuid4()),
        "thread_id": thread_id,
        "sender": "llm",
        "message": response
    }
    supabase.table("chat_messages").insert(llm_msg).execute()


def handle_llm_response(thread_id):
    history = get_message_history(thread_id)
    return _agent(thread_id, history)


