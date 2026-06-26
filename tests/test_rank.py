from tools.job_tool import fetch_jobs, rank_job

profile = {
    "summary": "AI Engineer",
    "skills": [
        "Python",
        "Machine Learning",
        "PyTorch",
        "NLP"
    ]
}

jobs = fetch_jobs()

job = rank_job(profile, jobs[0])

print(job)