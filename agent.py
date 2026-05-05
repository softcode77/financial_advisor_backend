# agent.py

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv


load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Create agent once (globally)
prompt = (
    "You are a helpful financial adviser who will advise users what to invest in "
    "based on their location and saving. If a user asks non investment related queries, politely decline."
)

memory = MemorySaver()
model = init_chat_model("anthropic:claude-3-5-sonnet-latest")
search = TavilySearch(max_results=2)
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory, prompt=prompt)

def _agent(thread_id: str, message_history: list[dict]) -> str:
    """
    message_history should be a list of {"sender": ..., "message": ...}
    """
    # Lanhchain format is {"role": "user" or "assistant", "content": ...}
    # List comprehension to convert message into dictionary so the agent can understand it. 
    langchain_messages = [
        {"role": "user" if message["sender"] == "user" else "assistant", "content": message["message"]}  for message in message_history
    ]

    config = {"configurable": {"thread_id": thread_id}}

    response = None
    for step in agent_executor.stream({"messages": langchain_messages}, config, stream_mode="values"):
        response = step["messages"][-1].content

    return response
