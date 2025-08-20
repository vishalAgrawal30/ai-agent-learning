from fastapi import FastAPI, Header
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from leave_balance import graph

app = FastAPI(title="Stock & Leave Chatbot API")

# Request/Response Models
class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    response: str

@app.post("/api/v1/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest
):
    # Prepare user message
    state_messages = [HumanMessage(content=request.text)]

    # Run LangGraph
    state = graph.invoke({"messages": state_messages})

    # Always a dict with "messages"
    last_message = state["messages"][-1]

    return ChatResponse(response=last_message.content)
