from tools.resume_tool import process_resume
from agents.planner_agent import planner_agent
from agents.tool_selector_agent import tool_selector_agent
from agents.reflection_agent import reflection_agent
from agents.executor_agent import executor_agent

from tools.job_tool import search_and_rank_jobs


# -------------------------
# CONFIGURATION
# -------------------------

MAX_ITERATIONS = 1

RESUME_PATH = "resume.pdf"


# -------------------------
# MEMORY
# -------------------------

memory = {
    "previous_searches": 0,
    "cover_letters_generated": 0,
    "resume_improvements": 0,
    "history": []
}


# -------------------------
# STEP 1 : Resume Agent
# -------------------------

print("\n========== Resume Agent ==========\n")

profile = process_resume(RESUME_PATH)


print("Resume processed.\n")


# -------------------------
# STEP 2 : Planner
# -------------------------

print("\n========== Planner ==========\n")

plan = planner_agent(profile)

goal = plan["goal"]

print(plan)

# -------------------------
# Resume Quality Decision
# -------------------------

if goal == "Improve Resume":

    print("\nPlanner decided to improve the resume first.\n")

    from tools.resume_improver_tool import improve_resume

    improvements = improve_resume(profile)

    print("\nResume Improvement Suggestions\n")

    print(improvements)

    # Next step:
    # Send email with these suggestions

    exit()

# -------------------------
# STEP 3 : Tool Selector
# -------------------------



ranked_jobs = []


# -------------------------
# AUTONOMOUS LOOP
# -------------------------

for iteration in range(MAX_ITERATIONS):

    print("\n" + "=" * 60)
    print(f"Iteration {iteration + 1}")
    print("=" * 60)

    # -------------------------
    # Search Jobs
    # -------------------------

    if not ranked_jobs:

        ranked_jobs = search_and_rank_jobs(profile)

        memory["previous_searches"] += 1

    # -------------------------
    # Reflection
    # -------------------------

    decision = reflection_agent(
        profile,
        ranked_jobs,
        goal,
        memory
    )

    print("\nReflection Decision\n")
    print(decision)

    memory["history"].append(decision)

    # -------------------------
    # Execute
    # -------------------------

    result = executor_agent(
        decision,
        profile,
        ranked_jobs,
        memory
    )

    print("\nExecution Result\n")
    print(result)

    action = decision["decision"]

    # -------------------------
    # Update Memory
    # -------------------------

    if action == "generate_cover_letter":

        memory["cover_letters_generated"] += 1

        break

    elif action == "improve_resume":

        memory["resume_improvements"] += 1

        break

    elif action == "continue_job_search":

        ranked_jobs = []

        continue

    elif action == "stop":

        print("\nGoal completed.")

        break

print("\n==============================")
print("Autonomous Execution Finished")
print("==============================")