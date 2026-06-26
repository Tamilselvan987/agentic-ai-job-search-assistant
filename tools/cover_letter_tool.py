import requests
import json
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def generate_cover_letter(profile, job):
    """
    Generate a personalized cover letter
    using the candidate profile and job.
    """

    prompt = f"""
You are writing a professional cover letter.

You MUST ONLY use information from the Candidate Profile.

Candidate Profile

{json.dumps(profile, indent=2)}

Job Information

Title:
{job["title"]}

Company:
{job["company"]}

Job Match Analysis

Strengths:
{job["strengths"]}

Missing Skills:
{job["missing_skills"]}

Reason for Match:
{job["reason"]}

Rules
- If the candidate does not clearly match the job, write a polite but honest cover letter without exaggerating qualifications.
- Do NOT mention any technology, framework, certification, project, or experience unless it appears in the Candidate Profile.
- Use ONLY facts from the Candidate Profile.
- NEVER claim the candidate has skills that are not listed.
- NEVER invent projects.
- NEVER invent experience.
- NEVER invent responsibilities.
- NEVER copy text from the job description.
- If a required skill is missing, do not pretend the candidate has it.
- Keep the letter under 200 words.
- Make it professional and concise.

Return ONLY the cover letter.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0
        }
    )

    return response.json()["response"]