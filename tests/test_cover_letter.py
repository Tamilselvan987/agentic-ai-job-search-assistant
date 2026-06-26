from tools.job_tool import search_and_rank_jobs
from tools.cover_letter_tool import generate_cover_letter

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
        "AI Engineer"
    ]
}

jobs = search_and_rank_jobs(profile)

letter = generate_cover_letter(
    profile,
    jobs[0]
)

print(letter)