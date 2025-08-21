from fastapi import FastAPI, Header
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from chatbot_graph import graph
from typing import Optional

# Import your leave_balance_tool (adjust import path if needed)
# from agents import check_leave_balance
import agents  

app = FastAPI(title="Stock & Leave Chatbot API")

# Request/Response Models
class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    response: str

@app.post("/api/v1/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    authorization: Optional[str] = Header(None)   # <-- read header
):
    # 🔹 Attach token to your tool
    if authorization:
        agents.set_auth_token(authorization)
        print(f"Received auth_token: {authorization}")

    # Prepare user message
    state_messages = [HumanMessage(content=request.text)]

    # Run LangGraph
    state = graph.invoke({"messages": state_messages})

    # Always a dict with "messages"
    last_message = state["messages"][-1]

    return ChatResponse(response=last_message.content)
