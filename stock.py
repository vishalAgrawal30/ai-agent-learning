from dotenv import load_dotenv
load_dotenv()

from typing import Annotated
from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START,END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

class State(TypedDict):
    messages:Annotated[list,add_messages]


@tool
def get_Stock_price(symbol : str)->float:
    """Get the stock price for a given stock symbol (e.g., SENSEX, MSFT, RIL)."""
    return {
        "MSFT":750.25,
        "RIL":5820.52,
        "AMZN":158.0,
        "SENSEX":81500.02
    }.get(symbol,0.0)

tools = [get_Stock_price]

llm = init_chat_model("google_genai:gemini-2.0-flash")
llm_with_tools = llm.bind_tools(tools)

def chatbot(state:State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(State)

builder.add_node(chatbot)
builder.add_node('tools',ToolNode(tools))

builder.add_edge(START,"chatbot")
builder.add_conditional_edges("chatbot",tools_condition)
builder.add_edge("tools","chatbot")
graph = builder.compile()