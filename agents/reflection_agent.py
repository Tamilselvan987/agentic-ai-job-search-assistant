import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def reflection_agent(profile, ranked_jobs, goal, memory):
    """
    Reviews the current progress and decides
    what the agent should do next.
    """

    prompt = f"""
You are the Reflection Agent in an autonomous Job Search AI system.

Your responsibility is NOT to solve the problem.

Your responsibility is ONLY to decide the next best action.

Current Goal

{goal}

Candidate Profile

{json.dumps(profile, indent=2)}

Top Ranked Jobs

{json.dumps(ranked_jobs[:5], indent=2)}

Memory

{json.dumps(memory, indent=2)}

Return ONLY valid JSON.

Format

{{
    "decision":"",
    "reason":"",
    "confidence":0
}}

Allowed Decisions

- continue_job_search
- generate_cover_letter
- improve_resume
- stop

Rules
-If at least one job has a score >= 80,
choose "generate_cover_letter".
-Only choose "continue_job_search"
when no job scores above 70.
- Think like an autonomous AI agent.
- Use ONLY the provided information.
- If the top-ranked jobs are good enough,
  choose generate_cover_letter.
- If the resume clearly needs improvement,
  choose improve_resume.
- If no useful jobs were found,
  choose continue_job_search.
- If the goal has already been completed,
  choose stop.
- Do NOT invent information.
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