from agents.executor_agent import executor_agent

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

ranked_jobs = [
    {
        "title": "Senior AI Engineer",
        "company": "OpenAI",
        "description": "AI Engineer role",
        "score": 95,
        "strengths": [
            "Python",
            "Machine Learning"
        ],
        "missing_skills": [
            "Docker"
        ],
        "reason": "Excellent match"
    }
]

memory = {}

decision = {
    "decision": "generate_cover_letter"
}

result = executor_agent(
    decision,
    profile,
    ranked_jobs,
    memory
)

print(result)