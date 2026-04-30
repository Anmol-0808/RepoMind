from agents.agent import app

print("\n🤖 RepoMind Agent (type 'exit' to quit)\n")

state = {
    "messages": [],
    "response": "",
    "last_repo_topic": ""
}

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    state["messages"].append(user_input)

    result = app.invoke(state)
    state["last_repo_topic"] = result.get("last_repo_topic", state["last_repo_topic"])

    state["messages"].append(result["response"])

    print("\nAI:\n")

    for char in result["response"]:
        print(char, end="", flush=True)

    print("\n")