from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal

load_dotenv()

client = OpenAI()

class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool

class CodeAccuracyResponse(BaseModel):
    accuracy_percentage: str

class State(TypedDict):
    user_query: str
    llm_result: str | None
    accuracy_percentage: str | None
    is_coding_question: bool | None
    max_retries: int 


def classify_message(state: State):
    print("⚠️ classify_query")
    query = state["user_query"]

    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to detect if the user's query is
    related to coding question or not.
    Return the response in specified JSON boolean only.
    """

    # Structured Outputs / Responses
    # beta version
    response = client.beta.chat.completions.parse(
        model="gpt-4.1-nano",
        response_format=ClassifyMessageResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )

    is_coding_question = response.choices[0].message.parsed.is_coding_question

    state["is_coding_question"] = is_coding_question

    return state


def router_query(state: State) -> Literal["general_query", "coding_query"]:
    print("⚠️ router_query")
    is_coding = state["is_coding_question"]

    if is_coding:
        return "coding_query"
    
    return "general_query"


def general_query(state: State):
    print("⚠️ general_query")
    query = state["user_query"]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": query}
        ]
    )

    state["llm_result"] = response.choices[0].message.content

    return state


def coding_query(state: State):
    print("⚠️ coding_query")
    query = state["user_query"]

    SYSTEM_PROMPT = """
        You are a Coding Expert Agent
    """

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )

    state["llm_result"] = response.choices[0].message.content

    return state


def coding_validate_query(state:State):
    print("⚠️ coding_validate_query")
    query = state["user_query"]
    llm_code = state["llm_result"]

    SYSTEM_PROMPT = f"""
        You are expert in calculating accuracy of the code according to the question.
        Return the percentage of accuracy
        
        User Query: {query}
        Code: {llm_code}
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4.1",
        response_format=CodeAccuracyResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]
    )

    state["accuracy_percentage"] = response.choices[0].message.parsed.accuracy_percentage
    return state


def check_accuracy(state: State) -> Literal[END, "regenerate_coding"]:
    print("⚠️ check_accuracy")
    accuracy = state["accuracy_percentage"]
    max_tries = state["max_retries"]

    if int(accuracy.strip('%')) < 95 and max_tries < 2:
        return "regenerate_coding"
    else :
        return END


def regenerate_coding(state: State):
    print("⚠️ regenerate_coding")
    query = state["user_query"]

    SYSTEM_PROMPT = f"""
        You are an coding expert who is writing code for more than 15 years. Your task is to generate the code from the user query. Write the code with 100% accuracy
        
        User Query: {query}
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]
    )

    print("\nresponse.choices[0].message.content:\n",response.choices[0].message.content)

    print("\nstate:\n", state)

    state["llm_result"] = response.choices[0].message.content
    state["max_retries"] = state.get("max_retries", 0) + 1

    return state

graph_builder = StateGraph(State)

# Define Nodes

graph_builder.add_node("classify_message", classify_message)

graph_builder.add_node("router_query", router_query)

graph_builder.add_node("general_query", general_query)

graph_builder.add_node("coding_query", coding_query)

graph_builder.add_node("coding_validate_query", coding_validate_query)

graph_builder.add_node("check_accuracy", check_accuracy)

graph_builder.add_node("regenerate_coding", regenerate_coding)


# Edges

graph_builder.add_edge(START, "classify_message")

graph_builder.add_conditional_edges( "classify_message", router_query)

graph_builder.add_edge("general_query", END)

graph_builder.add_edge("coding_query", "coding_validate_query")

graph_builder.add_conditional_edges("coding_validate_query", check_accuracy)

graph_builder.add_edge("regenerate_coding", "coding_validate_query")

graph = graph_builder.compile()

def main():
    user = input(">")

    _state: State = {
        "user_query": user,
        "accuracy_percentage": None,
        "is_coding_question": False,
        "llm_result": None,
        "max_retries": 0
    }

    response = graph.invoke(_state)

    print(response)

main()

