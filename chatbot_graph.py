from dotenv import load_dotenv
from agents import get_Stock_price,check_leave_balance

load_dotenv()

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from state import State


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