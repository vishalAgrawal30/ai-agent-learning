from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI(title="Header Checker API")

class ChatRequest(BaseModel):
    text: str

@app.post("/api/v1/chat")
async def chat_endpoint(request: Request, body: ChatRequest):
    # Get all headers
    headers = dict(request.headers)

    # Print headers in console
    print("==== Incoming Request Headers ====")
    for k, v in headers.items():
        print(f"{k}: {v}")
    print("=================================")

    # Detect client from User-Agent
    user_agent = headers.get("user-agent", "").lower()
    if "postman" in user_agent:
        client = "Postman"
    elif "thunder" in user_agent:
        client = "Thunder Client"
    else:
        client = "Unknown Client"

    return {
        "message": f"Hello! You are calling from {client}.",
        "received_headers": headers,
        "body": body.dict()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
