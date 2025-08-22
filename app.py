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
    response: dict  # response will be a dict


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    authorization: Optional[str] = Header(None)  # JSON string in Authorization header
):
    # 1️⃣ Call leave_balance tool if authorization is provided
    leave_balance_response = None
    if authorization:
        leave_balance_response = leave_balance.invoke(authorization)

    # 2️⃣ Build chatbot state messages
    state_messages = [HumanMessage(content=request.text)]

    # If we have leave balance, feed it into the chatbot context
    if leave_balance_response:
        state_messages.append(
            HumanMessage(content=f"Leave balance fetched: {json.dumps(leave_balance_response)}")
        )

    # 3️⃣ Run LangGraph chatbot
    state = graph.invoke({"messages": state_messages})
    last_message = state["messages"][-1].content

    # 4️⃣ Combine chatbot and raw leave balance response
    if leave_balance_response:
        final_response = {
            "chatbot": last_message,
            "leave_balance": leave_balance_response
        }
    else:
        final_response = {"chatbot": last_message}

    return ChatResponse(response=final_response)
