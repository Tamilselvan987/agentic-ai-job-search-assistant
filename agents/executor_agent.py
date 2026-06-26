from tools.cover_letter_tool import generate_cover_letter
from tools.resume_improver_tool import improve_resume
from tools.job_tool import search_and_rank_jobs
import json

def executor_agent(decision, profile, ranked_jobs, memory):
    """
    Executes the decision produced by the Reflection Agent.
    """

    action = decision["decision"]

    print(f"\nExecutor Decision: {action}\n")

    # -------------------------
    # Generate Cover Letter
    # -------------------------
    if action == "generate_cover_letter":

        if not ranked_jobs:
            return {
                "status": "failed",
                "message": "No ranked jobs available."
            }

        letter = generate_cover_letter(
            profile,
            ranked_jobs[0]
        )

        return {
            "status": "success",
            "action": action,
            "cover_letter": letter
        }

    # -------------------------
    # Improve Resume
    # -------------------------
    elif action == "improve_resume":

        improvements = improve_resume(profile)

        from tools.email_tool import send_email

        body = f"""
    Our AI Planner decided that your resume should be improved before searching for jobs.

    Resume Suggestions

    {json.dumps(improvements, indent=4)}

    Please update your resume and upload it again.

    Regards,

    Autonomous AI Job Search Assistant
    """

        send_email(
            "Resume Improvement Suggestions",
            body
        )

        return {

            "status": "success",

            "action": action,

            "resume_improvements": improvements,

            "email_sent": True
        }

    # -------------------------
    # Continue Search
    # -------------------------
    elif action == "continue_job_search":

        jobs = search_and_rank_jobs(profile)

        return {
            "status": "success",
            "action": action,
            "jobs": jobs
        }

    # -------------------------
    # Stop
    # -------------------------
    elif action == "stop":

        return {
            "status": "completed",
            "message": "Goal completed."
        }

    # -------------------------
    # Unknown
    # -------------------------
    else:

        return {
            "status": "failed",
            "message": f"Unknown action: {action}"
        }