from fastapi import FastAPI, Header
from pydantic import BaseModel
from chatbot_graph import graph
from langchain_core.messages import HumanMessage
from typing import Optional
from agents import leave_balance
import json

app = FastAPI(title="Stock & Leave Chatbot API")

# Request/Response Models
class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    response: str


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    x_user_context: Optional[str] = Header(None, alias="x-user-context",convert_underscores=False)  # ✅ force exact header match
):
    leave_balance_response = None

    if x_user_context:
        leave_balance_response = leave_balance.invoke(x_user_context)
    # Prepare chatbot state
    state_messages = [HumanMessage(content=request.text)]

    if leave_balance_response:
        state_messages.append(
            HumanMessage(content=f"Leave balance fetched: {json.dumps(leave_balance_response)}")
        )

    # Run chatbot graph
    state = graph.invoke({"messages": state_messages})
    last_message = state["messages"][-1].content

    return ChatResponse(response=last_message)
