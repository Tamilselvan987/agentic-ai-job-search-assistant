import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def planner_agent(state):
    """
    Planner Agent

    Decides the next GOAL based on the
    candidate profile and previous memory.
    """



    prompt = f"""
You are the Planner Agent of an autonomous career assistant.

Your job is NOT to execute tools.

Your job is ONLY to decide the next goal.

Current Shared State

{json.dumps(state, indent=2)}

Resume Quality Decision Rules

If resume_quality is "weak":

- Goal = Improve Resume

Reason:
The resume should be improved before searching for jobs to increase the candidate's chances.

If resume_quality is "strong":

- Goal = Search Jobs

Reason:
The resume is strong enough to begin searching for relevant jobs.

Always use the value of resume_quality from the shared state.



Available Goals:

1. Search Jobs
2. Evaluate Jobs
3. Generate Cover Letters
4. Improve Resume
5. Notify User
6. Apply To Job
7. Finish

Think step by step.

Choose ONLY ONE next goal.

Return ONLY valid JSON.

Format:

{{
    "goal":"",
    "priority":"",
    "reason":"",
    "expected_output":""
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