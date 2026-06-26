from agents.reflection_agent import reflection_agent

state = {

    "planner_output": {
        "goal": "Search Jobs"
    },

    "selected_tool": {
        "tool": "job_search_tool"
    },

    "jobs": [
        {
            "title": "AI Engineer"
        },
        {
            "title": "ML Engineer"
        }
    ]
}

result = reflection_agent(state)

print(result)