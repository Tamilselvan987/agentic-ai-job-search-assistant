from agents.tool_selector_agent import tool_selector_agent

state = {
    "planner_output": {
        "goal": "Search Jobs"
    }
}

result = tool_selector_agent(state)

print(result)