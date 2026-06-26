import requests
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
# -------------------------
# Remotive Jobs
# -------------------------
def fetch_remotive_jobs():
    try:
        url = "https://remotive.com/api/remote-jobs"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()["jobs"]

        jobs = []

        for job in data:
            jobs.append({
                "title": job.get("title", ""),
                "company": job.get("company_name", ""),
                "description": job.get("description", ""),
                "location": job.get("candidate_required_location", ""),
                "url": job.get("url", ""),
                "source": "Remotive"
            })

        return jobs
    except Exception as e:
        print("Remotive Error:", e)
        return []
# -------------------------
# RemoteOK Jobs
# -------------------------
def fetch_remoteok_jobs():
    try:
        url = "https://remoteok.com/api"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        jobs = []

        # first object contains metadata
        for job in data[1:]:

            jobs.append({
                "title": job.get("position", ""),
                "company": job.get("company", ""),
                "description": job.get("description", ""),
                "location": "Remote",
                "url": job.get("url", ""),
                "source": "RemoteOK"
            })

        return jobs

    except Exception as e:
        print("RemoteOK Error:", e)
        return []


# -------------------------
# Combine Sources
# -------------------------
def fetch_jobs():

    jobs = []

    jobs.extend(fetch_remotive_jobs())
    jobs.extend(fetch_remoteok_jobs())

    print(f"\nFetched {len(jobs)} jobs")

    return jobs

import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def rank_jobs(profile, jobs):
    """
    Rank multiple jobs in ONE LLM call.
    """

    # -------------------------
    # Compact Jobs
    # -------------------------

    compact_jobs = []

    for i, job in enumerate(jobs):

        compact_jobs.append({
            "index": i,
            "title": job["title"],
            "company": job["company"],
            "description": job["description"][:1000],
            "location": job["location"]
        })

    prompt = f"""
You are an expert technical recruiter.

Candidate Profile

{json.dumps(profile, indent=2)}

Jobs

{json.dumps(compact_jobs, indent=2)}

Evaluate EVERY job independently.

Return ONLY valid JSON.

Format

{{
    "jobs":[
        {{
            "index":0,
            "score":0,
            "strengths":[],
            "missing_skills":[],
            "reason":""
            
        }}
    ]
}}

Evaluation Criteria

1. Domain Match (40%)

2. Skills Match (30%)

3. Experience Match (20%)

4. Projects Match (10%)

Scoring

90-100 Excellent Match

70-89 Strong Match

50-69 Partial Match

30-49 Weak Match

0-29 Different Domain

Field Requirements

- "strengths":
  - List 2–5 candidate strengths that directly match the job requirements.
  - Use only information from the Candidate Profile.

- "missing_skills":
  - List only the top 2–5 important missing skills.
  - Do not include skills the candidate already has.

- "reason":
  - Write 1–2 concise sentences explaining the score.
  - Do NOT leave this field empty.

Rules

- Score must be between 0 and 100.

- If the job belongs to another domain,
  score MUST be below 30.

- NEVER invent skills.

- NEVER invent projects.

- NEVER invent experience.

- Use ONLY the Candidate Profile.

- Return ONE result for EVERY job.

- The root JSON object MUST contain the key "jobs".

- Do NOT return explanations outside JSON.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "temperature": 0,
            "options": {
                "num_predict": 4096
            }
        }
    )

    # -------------------------
    # Debug
    # -------------------------

    raw_response = response.json()["response"]

    print("\n========== RAW RESPONSE ==========")
    print(raw_response)
    print("==================================\n")

    response_json = json.loads(raw_response)

    print("\n========== PARSED JSON ==========")
    print(response_json)
    print(type(response_json))
    print("=================================\n")

    results = response_json["jobs"]

    ranked_jobs = []

    for result in results:

        job = jobs[result["index"]]

        job["score"] = result["score"]
        job["strengths"] = result["strengths"]
        job["missing_skills"] = result["missing_skills"]
        job["reason"] = result["reason"]

        ranked_jobs.append(job)

    return ranked_jobs

def search_and_rank_jobs(profile, limit=10, batch_size=3):
    """
    Fetch jobs, filter them, rank them using the LLM
    in batches, and return the best matches.
    """

    # -------------------------
    # Fetch Jobs
    # -------------------------
    jobs = fetch_jobs()

    # -------------------------
    # Build Search Keywords
    # -------------------------
    keywords = []

    keywords.extend(profile.get("preferred_roles", []))
    keywords.extend(profile.get("skills", []))

    if profile.get("domain"):
        keywords.append(profile["domain"])

    keywords = [k.lower() for k in keywords]

    # -------------------------
    # Quick Python Filter
    # -------------------------
    filtered_jobs = []

    for job in jobs:

        text = (
            job.get("title", "") +
            " " +
            job.get("description", "")
        ).lower()

        if any(keyword in text for keyword in keywords):
            filtered_jobs.append(job)

    # -------------------------
    # Fallback
    # -------------------------
    if not filtered_jobs:

        print("No keyword matches found. Using first jobs.")

        jobs_to_rank = jobs[:limit]

    else:

        print(f"Filtered {len(filtered_jobs)} relevant jobs.")

        jobs_to_rank = filtered_jobs[:limit]

    # -------------------------
    # Batch Ranking
    # -------------------------
    ranked_jobs = []

    for i in range(0, len(jobs_to_rank), batch_size):

        batch = jobs_to_rank[i:i + batch_size]

        print(
            f"Ranking Batch {i//batch_size + 1} "
            f"({len(batch)} jobs)"
        )

        try:

            ranked_batch = rank_jobs(profile, batch)

            ranked_jobs.extend(ranked_batch)

        except Exception as e:

            print(f"Batch {i//batch_size + 1} failed")
            print(e)

    # Fallback: rank each job individually
            for job in batch:
                try:
                    ranked_jobs.extend(rank_jobs(profile, [job]))
                except Exception:
                    pass

    # -------------------------
    # Sort Results
    # -------------------------
    ranked_jobs.sort(
        key=lambda job: job["score"],
        reverse=True
    )

    return ranked_jobs