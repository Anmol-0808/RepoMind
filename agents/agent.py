from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import os
from dotenv import load_dotenv
import re

from agents.tools import (
    repo_qa_tool,
    repo_improvement_tool,
    repo_code_fix_tool
)

load_dotenv()


class AgentState(TypedDict):
    messages: List[str]
    response: str
    last_repo_topic: str


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

    code_keywords = [
        "write", "implement", "fix",
        "refactor", "rewrite",
        "improve code", "optimize code"
    ]

    follow_up_words = [
        "that", "this", "it",
        "where", "why", "how",
        "simplify", "explain more",
        "what about that"
    ]

    if contains_word(lower_query, ["hi", "hello", "hey"]):
        return {
            "messages": state["messages"],
            "response": "Hey 👋 I’m RepoMind — your AI assistant for this codebase. Ask me anything about your project.",
            "last_repo_topic": state.get("last_repo_topic", "")
        }

    if contains_word(lower_query, follow_up_words) and state.get("last_repo_topic"):
        user_query = f"""
Previous topic discussed:
{state["last_repo_topic"]}

Current follow-up question:
{user_query}
"""

    if contains_word(lower_query, code_keywords):
        result = repo_code_fix_tool.invoke(user_query)
        return {
            "messages": state["messages"],
            "response": result,
            "last_repo_topic": user_query
        }

    if contains_word(lower_query, improvement_keywords):
        result = repo_improvement_tool.invoke(user_query)
        return {
            "messages": state["messages"],
            "response": result,
            "last_repo_topic": user_query
        }

    if contains_word(lower_query, repo_hint_words):
        result = repo_qa_tool.invoke(user_query)
        return {
            "messages": state["messages"],
            "response": result,
            "last_repo_topic": user_query
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
            "response": "Hey! 👋 What part of the repo do you want to explore?",
            "last_repo_topic": state.get("last_repo_topic", "")
        }

    elif decision == "REPO_QUESTION":
        result = repo_qa_tool.invoke(user_query)
        return {
            "messages": state["messages"],
            "response": result,
            "last_repo_topic": user_query
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
            "response": response,
            "last_repo_topic": state.get("last_repo_topic", "")
        }


graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)

graph.set_entry_point("agent")
graph.add_edge("agent", END)

app = graph.compile()