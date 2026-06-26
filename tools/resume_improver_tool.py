import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def improve_resume(profile, ranked_jobs=None):
    """
    Resume Improvement Tool

    Mode 1:
        If no jobs are provided, analyze the resume only.

    Mode 2:
        If jobs are provided, compare the resume against
        the top matching jobs and suggest improvements.
    """

    if ranked_jobs is None:
        ranked_jobs = []

    top_jobs = ranked_jobs[:5]

    # --------------------------------------------------
    # Resume Only
    # --------------------------------------------------

    if len(top_jobs) == 0:

        prompt = f"""
You are an expert technical recruiter and resume reviewer.

Candidate Profile

{json.dumps(profile, indent=2)}

The candidate has NOT searched for jobs yet.

Review ONLY the resume.

Return ONLY valid JSON.

Format

{{
    "missing_skills": [],
    "recommended_projects": [],
    "resume_improvements": [],
    "ats_keywords": [],
    "overall_feedback": ""
}}

Rules

1. Use ONLY the Candidate Profile.

2. NEVER list a skill under "missing_skills" if it already exists in the Candidate Profile.

3. missing_skills must contain ONLY important technical skills that are NOT present in the resume.

4. NEVER recommend projects that already exist in the resume.

5. resume_improvements should focus on:
   - Professional Summary
   - Experience
   - Achievements
   - Resume Structure
   - Certifications
   - Projects

6. ATS keywords should be general software industry keywords.

7. Do NOT invent experience.

8. Do NOT invent completed projects.

9. Return concise recommendations.

10. Before returning missing_skills,
    compare them against profile["skills"].
    If a skill already exists,
    DO NOT include it.
"""

    # --------------------------------------------------
    # Resume + Jobs
    # --------------------------------------------------

    else:

        prompt = f"""
You are an expert technical recruiter and resume reviewer.

Candidate Skills

{json.dumps(profile.get("skills", []), indent=2)}

Candidate Projects

{json.dumps(profile.get("projects", []), indent=2)}

Candidate Experience

{json.dumps(profile.get("experience", []), indent=2)}

Candidate Summary

{profile.get("summary", "")}

Top Matching Jobs

{json.dumps(top_jobs, indent=2)}

Your task is to compare the resume against the jobs.

Return ONLY valid JSON.

Format

{{
    "missing_skills": [],
    "recommended_projects": [],
    "resume_improvements": [],
    "ats_keywords": [],
    "overall_feedback": ""
}}

Rules

1. Use ONLY the Candidate Profile and Top Matching Jobs.

2. Compare the candidate's skills against the job requirements.

3. NEVER list a skill under missing_skills if it already exists in profile["skills"].

4. missing_skills should contain ONLY skills that appear in multiple jobs AND are absent from the resume.

5. NEVER recommend projects already present in the resume.

6. ATS keywords should come ONLY from the job descriptions.

7. Do NOT invent experience.

8. Do NOT invent completed projects.

9. Prioritize improvements that appear across multiple jobs.

10. Before returning missing_skills,
    verify that each skill is absent from the candidate profile.
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