from tools.job_tool import search_and_rank_jobs

profile = {
    "domain": "AI / Machine Learning",

    "summary": "AI Engineer",

    "skills": [
        "Python",
        "Machine Learning",
        "PyTorch",
        "NLP"
    ],

    "projects": [
        "Fake News Detection"
    ],

    "experience": [
        "ML Intern"
    ],

    "preferred_roles": [
        "AI Engineer",
        "Machine Learning Engineer"
    ]
}

jobs = search_and_rank_jobs(profile)

print("\nTop Ranked Jobs\n")

for job in jobs:

    print("=" * 60)

    print("Score:", job["score"])

    print("Title:", job["title"])

    print("Company:", job["company"])

    print("Strengths:", job["strengths"])

    print("Missing Skills:", job["missing_skills"])

    print("Reason:", job["reason"])

    print("=" * 60)