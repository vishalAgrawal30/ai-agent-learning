from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional
import json
import sample  # import your sample.py

app = FastAPI(title="Sample JSON Header Test")

class ChatRequest(BaseModel):
    text: str

@app.post("/api/v1/chat")
def chat_endpoint(
    request: ChatRequest,
    authorization: Optional[str] = Header(None)  # read header
):
    if authorization:
        try:
            # Convert JSON string → Python dict
            auth_data = json.loads(authorization)
            print("Parsed Auth JSON in FastAPI:", auth_data)

            # Pass token to sample.py
            sample.set_auth_token(auth_data.get("authToken"))

            # Optional: print full auth_data
            sample.print_auth_data(auth_data)

        except json.JSONDecodeError:
            print("❌ Invalid JSON in Authorization header")
    
    return {"status": "Header received and printed successfully"}
