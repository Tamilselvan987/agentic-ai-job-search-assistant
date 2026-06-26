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


    elif action == "improve_resume":

        improvements = improve_resume(profile)

        from tools.email_tool import send_email

        body = f"""
Our AI Planner decided that your resume should be improved before searching for jobs.

==============================
RESUME SUGGESTIONS
==============================

Missing Skills
--------------
{chr(10).join("• " + skill for skill in improvements["missing_skills"])}

Recommended Projects
--------------------
{chr(10).join("• " + project for project in improvements["recommended_projects"])}

Resume Improvements
-------------------
{chr(10).join("• " + item for item in improvements["resume_improvements"])}

ATS Keywords
------------
{", ".join(improvements["ats_keywords"])}

Overall Feedback
----------------
{improvements["overall_feedback"]}

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


    else:

        return {
            "status": "failed",
            "message": f"Unknown action: {action}"
        }