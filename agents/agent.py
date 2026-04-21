from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import os
from dotenv import load_dotenv
import re
from agents.tools import repo_qa_tool
from agents.tools import repo_qa_tool, repo_improvement_tool
load_dotenv()


class AgentState(TypedDict):
    messages: List[str]
    response: str


def get_llm():
    return ChatOpenAI(
        model="gpt-5",
        temperature=0.2,
        streaming=True,
        api_key=os.getenv("OPENAI_API_KEY")
    )


def contains_word(text, words):
    return any(re.search(rf"\b{word}\b", text) for word in words)


def agent_node(state: AgentState):

    llm = get_llm()
    user_query = state["messages"][-1]
    lower_query = user_query.lower()


    repo_hint_words = [
        "repo", "project", "code", "file", "api",
        "backend", "frontend", "function", "class",
        "auth", "login", "route", "model", "database",
        "structure", "flow"
    ]

    improvement_keywords = [
    "improve", "better", "optimize",
    "issue", "problem", "scalable",
    "refactor", "enhance"
]

    if contains_word(lower_query, improvement_keywords):
        result = repo_improvement_tool.invoke(user_query)
        return {
            "messages": state["messages"],
            "response": result
        }

    if contains_word(lower_query, repo_hint_words):
        result = repo_qa_tool.invoke(user_query)
        return {
            "messages": state["messages"],
            "response": result
        }


    decision_prompt = f"""
You are RepoMind, an AI assistant focused on a code repository.

Conversation so far:
{state["messages"][-5:]}

User message:
{user_query}

Classify intent:

- GREETING
- REPO_QUESTION
- GENERAL

IMPORTANT:
If unsure → REPO_QUESTION

Respond with ONE word only.
"""

    decision = llm.invoke(decision_prompt).content.strip()

    if decision == "GREETING":
        return {
            "messages": state["messages"],
            "response": "Hey! 👋 What part of the repo do you want to explore?"
        }

    elif decision == "REPO_QUESTION":
        result = repo_qa_tool.invoke(user_query)
        return {
            "messages": state["messages"],
            "response": result
        }

    else:
        response = ""

        for chunk in llm.stream(user_query):
            if hasattr(chunk, "content") and chunk.content:
                print(chunk.content, end="", flush=True)
                response += chunk.content

        print()

        return {
            "messages": state["messages"],
            "response": response
        }


graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)

graph.set_entry_point("agent")
graph.add_edge("agent", END)

app = graph.compile()