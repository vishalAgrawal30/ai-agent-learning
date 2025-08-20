from typing import TypedDict, List
from langchain_core.messages import HumanMessage

class State(TypedDict):
    messages: List[HumanMessage]
