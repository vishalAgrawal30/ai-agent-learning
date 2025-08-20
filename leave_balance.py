from dotenv import load_dotenv
import requests
from langchain_core.tools import tool

load_dotenv()

# ✅ Put a space after "PZN"
AUTH_TOKEN = "PZN eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJUQjEwMDEiLCJ0b2tlblZlcnNpb24iOjEzLCJpZCI6NDMyLCJ1c2VyVHlwZSI6ImlzRW1wbG95ZWUiLCJlbXBsb3llZUlkIjo0MjUsImNvbXBhbnlJZCI6NSwiaWF0IjoxNzU1NTk0NTU4fQ.OztB8sjlvY66oOo_tw5-gX_voes1PLvuUCy9Sn-IeznQoEIsBg9PFxQw7ahxvi7xaWKst5C71yhNiVividZwWQ"
API_URL = "https://uat.fuzionhr.com/api/v1/hrms/leaveApplication/getMyLeaveBalance"
    API_URL_PROD = "https://api.fuzionhr.com/api/v1/hrms/leaveApplication/getMyLeaveBalance"
AUTH_TOKEN_PROD = "PZN eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJUQjEwMTYiLCJ0b2tlblZlcnNpb24iOjIsImlkIjoyNTY1LCJ1c2VyVHlwZSI6ImlzRW1wbG95ZWUiLCJlbXBsb3llZUlkIjoyNTU4LCJjb21wYW55SWQiOjEsImlhdCI6MTc1NTY2MTY0OH0.tFP-4eLXKfq781WB4A44ng5sb37ZE-oNhfxRtgC9qGxYs1ttLRuCbOBJb0-3Mqf1WwWEB5mtiYB3X9lOFlbSuA"
DEVICE="cdeaf1a1-6447-46ac-8c9f-c0208383afaf"
@tool
def check_leave_balance(
    login_id: int , emp_id: int) -> dict:
    """Fetch leave balance for a given employee.
    Only use this tool if the user asks about leave balances."""

    # headers = {
    #     "accept": "application/json, text/plain, */*",
    #     "authorization": API_URL_PROD,
    #     "content-type": "application/json",
    #     "referer": "https://uat.fuzionhr.com/",
    #     "x-device-id": "a3c8e562-8642-42f7-ba3e-68c787e0c605",
    #     "x-fcm-token": "null",
    # }
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": API_URL_PROD,
        "content-type": "application/json",
        "referer": "https://techiebrothers.fuzionhr.com/",
        "x-device-id": DEVICE,
        "x-fcm-token": "null",
    }

    payload = {
        "loginId": login_id,
        "employeeId": emp_id
    }

    try:
        response = requests.post(API_URL_PROD, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed with {response.status_code}", "details": response.text}
    except Exception as e:
        return f"❌ API call failed: {e}"
    
@tool
def get_Stock_price(symbol : str)->float:
    """Get the stock price for a given stock symbol (e.g., SENSEX, MSFT, RIL)."""
    return {
        "MSFT":750.25,
        "RIL":5820.52,
        "AMZN":158.0,
        "SENSEX":81500.02
    }.get(symbol,0.0)

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage

# --- State ---
class State(TypedDict):
    messages: Annotated[list, add_messages]

# --- Register Tool ---
tools = [check_leave_balance,get_Stock_price]

llm = init_chat_model(
    "google_genai:gemini-2.0-flash"
)

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    result = llm_with_tools.invoke(state["messages"])
    return {"messages": state["messages"] + [result]}   # always append to "messages"

# --- Graph ---
builder = StateGraph(State)

builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")   # go back to chatbot after tool runs
builder.add_edge("chatbot", END)

graph = builder.compile()