from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START,END
from langgraph.prebuilt import ToolNode, tools_condition
from agents import get_Stock_price, check_leave_balance
from state import State
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage

load_dotenv()

# Register tools
tools = [get_Stock_price, check_leave_balance]

# LLM with tools
llm = init_chat_model("google_genai:gemini-2.0-flash")
llm_with_tools = llm.bind_tools(tools)


# Chatbot Node
def chatbot(state: State):
    user_msg = state["messages"][-1].content

    system_prompt = SystemMessage(content=(
        "You are a helpful assistant. "
        "If the user asks about stock prices, call `get_stock_price`. "
        "If the user mentions a quantity, calculate total cost. "
        "If the user asks about leave balances, call `check_leave_balance` "
        "using login_id and emp_id if available."
    ))

    # Don’t overwrite user message; prepend system message
    ai_msg = llm_with_tools.invoke([system_prompt] + state["messages"])

    return {"messages": state["messages"] + [ai_msg]}


# Build LangGraph
builder = StateGraph(State)
builder.add_node(chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")
builder.add_edge("chatbot", END)


graph = builder.compile()
