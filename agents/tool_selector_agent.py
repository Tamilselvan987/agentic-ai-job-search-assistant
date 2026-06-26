import json
import requests
TOOLS = [
    {
        "name": "job_search_tool",
        "purpose": "Search and rank jobs"
    },
    {
        "name": "cover_letter_tool",
        "purpose": "Generate a cover letter"
    },
    {
        "name": "resume_improver_tool",
        "purpose": "Improve the resume"
    }
]

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def tool_selector_agent(state):
    """
    Tool Selection Agent

    Chooses the best tool to achieve
    the Planner's goal.
    """

    prompt = f"""
You are the Tool Selection Agent.

The Planner has already decided the next goal.

Current Shared State:

{json.dumps(state, indent=2)}

Available Tools

{json.dumps(TOOLS, indent=2)}

Your task is to select ONLY ONE tool.

Think carefully.

Return ONLY valid JSON.

Format:

{{
    "tool": "",
    "confidence": 95,
    "reason": ""
}}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "temperature": 0
        }
    )

    return json.loads(response.json()["response"])