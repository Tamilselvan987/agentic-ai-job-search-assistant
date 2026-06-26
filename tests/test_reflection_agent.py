from agents.reflection_agent import reflection_agent

profile = {
    "domain": "AI / Machine Learning",
    "skills": ["Python", "Machine Learning", "PyTorch", "NLP"]
}

goal = "Search Jobs"

memory = {
    "previous_searches": 1,
    "cover_letters_generated": 0
}

ranked_jobs = [
    {
        "title": "Senior AI Engineer",
        "score": 92
    },
    {
        "title": "ML Engineer",
        "score": 88
    }
]

decision = reflection_agent(
    profile,
    ranked_jobs,
    goal,
    memory
)

print(decision)