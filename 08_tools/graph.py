from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import requests
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition 

load_dotenv()

@tool()
def add_two_numbers(a, b):
    """This tool adds two int numbers"""
    return a+b

@tool()
def subtract_two_numbers(a, b):
    """This tool subtracts two int numbers"""
    return a - b

@tool()
def multiply_two_numbers(a, b):
    """This tool multiply two int numbers"""
    return a * b

@tool()
def get_weather(city: str):
    """This tool returns the weather data about the given city"""

    url = f"https://wttr.in/{city.lower()}?format=%C+%t"

    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."

    return "Something went wrong"


class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = init_chat_model(model_provider="openai", model="gpt-4.1")

tools = [get_weather, add_two_numbers]

llm_with_tools = llm.bind_tools(tools)

def chatbot(state:State):
    message = llm_with_tools.invoke(state["messages"])

    return {"messages": [message]}

graph_builder = StateGraph(State)

tool_node = ToolNode(tools=tools)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()


def main():
    query = input("> ")

    _state = State( 
        messages=[{"role": "user", "content": query}]
    )

    for event in graph.stream(_state, stream_mode="values"):
        if "messages" in event:
            event["messages"][-1].pretty_print()



main()