import json
import os

MEMORY_FILE = "memory/memory.json"


def load_memory():
    """
    Load persistent memory.
    """

    if not os.path.exists(MEMORY_FILE):
        return {
            "history": [],
            "applied_jobs": [],
            "planner_decisions": [],
            "resume_versions": []
        }

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    """
    Save persistent memory.
    """

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


def add_history(action):
    """
    Store executed tool history.
    """

    memory = load_memory()

    memory["history"].append(action)

    save_memory(memory)


def add_planner_decision(decision):
    """
    Store planner output.
    """

    memory = load_memory()

    memory["planner_decisions"].append(decision)

    save_memory(memory)


def add_applied_job(job_title):
    """
    Store applied jobs.
    """

    memory = load_memory()

    if job_title not in memory["applied_jobs"]:
        memory["applied_jobs"].append(job_title)

    save_memory(memory)