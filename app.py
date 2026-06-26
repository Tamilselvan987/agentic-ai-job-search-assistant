import streamlit as st
import tempfile
import pandas as pd

from tools.resume_tool import process_resume
from agents.planner_agent import planner_agent
from agents.tool_selector_agent import tool_selector_agent
from agents.reflection_agent import reflection_agent
from agents.executor_agent import executor_agent

from tools.job_tool import search_and_rank_jobs


MAX_SEARCH_ITERATIONS = 2

st.set_page_config(
    page_title="Autonomous AI Job Search Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Autonomous AI Job Search Assistant")

st.markdown("---")

memory = {

    "previous_searches":0,

    "cover_letters_generated":0,

    "resume_improvements":0,

    "history":[]
}

def show_profile(profile):

    st.header("📄 Candidate Profile")

    col1,col2 = st.columns(2)

    with col1:

        st.subheader("Domain")

        st.write(profile.get("domain","Not Available"))

        st.subheader("Education")

        education = profile.get("education","")

        if education:

            st.write(education)

        else:

            st.info("Education not found.")


    with col2:

        st.subheader("Preferred Roles")

        roles = profile.get("preferred_roles",[])

        if roles:

            for role in roles:

                st.write("✔",role)

        else:

            st.info("No preferred roles identified.")



    st.subheader("Professional Summary")

    summary = profile.get("summary","")

    if summary:

        st.write(summary)

    else:

        st.info("Summary not available.")


    st.subheader("Skills")

    skills = profile.get("skills",[])

    if skills:

        st.write(", ".join(skills))

    else:

        st.info("No skills extracted.")

    st.subheader("💼 Experience")

    experience = profile.get("experience",[])

    if experience:

        for exp in experience:

            st.markdown(
                f"### {exp.get('title','Unknown Position')}"
            )

            st.write(
                "**Company:**",
                exp.get("company","Unknown")
            )

            st.write(
                "**Duration:**",
                exp.get(
                    "duration",
                    exp.get("dates","Not Available")
                )
            )

            if exp.get("description"):

                st.write(exp["description"])

            st.markdown("---")

    else:

        st.info("No experience found.")


    st.subheader("Projects")

    projects = profile.get("projects",[])

    if projects:

        for project in projects:

            st.write("•",project)

    else:

        st.info("No projects found.")

    st.markdown("---")


def show_jobs(ranked_jobs):

    st.header("💼 Top Job Matches")

    rows=[]

    for job in ranked_jobs:

        rows.append({

            "Score":job["score"],

            "Title":job["title"],

            "Company":job["company"],

            "Location":job.get("location",""),

            "Source":job.get("source","")

        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True
    )


def show_best_job(best):

    st.markdown("---")

    st.header("🏆 Best Match")

    st.write("###",best["title"])

    st.write("**Company:**",best["company"])

    st.write("**Score:**",best["score"])

    if best.get("url"):

        st.link_button(
            "🔗 Apply Now",
            best["url"]
        )

    st.subheader("Strengths")

    for s in best.get("strengths",[]):

        st.write("✔",s)

    st.subheader("Missing Skills")

    for s in best.get("missing_skills",[]):

        st.write("•",s)

    st.subheader("Reason")

    st.write(
        best.get(
            "reason",
            "No explanation available."
        )
    )

uploaded_file = st.file_uploader(

    "Upload your Resume (PDF)",

    type=["pdf"]

)

if uploaded_file is not None:

    temp_file = tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".pdf"

    )

    temp_file.write(uploaded_file.read())

    temp_file.close()

    if st.button("🚀 Start Autonomous Search"):
        ranked_jobs = []
        decision = None
        result = None


        with st.spinner("Analyzing Resume..."):

            profile = process_resume(temp_file.name)
        st.success("Resume analyzed successfully!")

        show_profile(profile)


        with st.spinner("Planner Agent Thinking..."):

            plan = planner_agent(profile)

        goal = plan["goal"]

        st.markdown("---")

        st.header("🧠 Planner Agent")

        st.success(f"Goal : {goal}")

        st.write(plan["reason"])


        if goal == "Improve Resume":

            st.warning(
                "Planner decided that the resume should be improved before searching for jobs."
            )

            decision = {

                "decision":"improve_resume"

            }

            with st.spinner("Improving Resume..."):

                result = executor_agent(

                    decision,

                    profile,

                    [],

                    memory

                )

            memory["resume_improvements"] += 1

            st.success(
                "Resume improvement suggestions generated."
            )

            if result.get("email_sent"):

                st.success(
                    "📧 Improvement suggestions have been emailed."
                )

            st.header("📄 Resume Suggestions")

            improvements = result["resume_improvements"]

            st.subheader("Missing Skills")

            for skill in improvements.get(
                "missing_skills",
                []
            ):

                st.write("•",skill)

            st.subheader("Recommended Projects")

            for project in improvements.get(
                "recommended_projects",
                []
            ):

                if isinstance(project,dict):

                    st.write(
                        f"• {project.get('title','')}"
                    )

                else:

                    st.write("•",project)

            st.subheader("Resume Improvements")
            for item in improvements.get(
                "resume_improvements",
                []
            ):
                if isinstance(item,dict):
                    st.write(
                        f"• {item.get('feedback','')}"
                    )
                else:
                    st.write("•",item)
            st.subheader("ATS Keywords")
            st.write(
                ", ".join(
                    improvements.get(
                        "ats_keywords",
                        []
                    )
                )
            )
            st.subheader("Overall Feedback")
            st.info(
                improvements.get(
                    "overall_feedback",
                    ""
                )
            )

            st.stop()

        with st.spinner("Selecting Best Tool..."):

            tool = tool_selector_agent(goal)

        st.header("🤖 Agent Execution")

        st.success("Resume Agent Completed")

        st.success(f"Planner Goal : {goal}")

        st.success(f"Tool Selected : {tool['tool']}")


        ranked_jobs = []

        decision = None

        result = None

        for iteration in range(MAX_SEARCH_ITERATIONS):

            st.markdown("---")

            st.info(
                f"🔄 Autonomous Search Iteration {iteration + 1}"
            )

            with st.spinner("Searching & Ranking Jobs..."):

                ranked_jobs = search_and_rank_jobs(profile)

            memory["previous_searches"] += 1

            st.success(f"{len(ranked_jobs)} Jobs Ranked")

            with st.spinner("Reflection Agent Thinking..."):

                decision = reflection_agent(

                    profile,

                    ranked_jobs,

                    goal,

                    memory

                )

            memory["history"].append(decision)

            st.success(

                f"Reflection Decision : {decision['decision']}"

            )

            if decision["decision"] == "continue_job_search":

                if iteration < MAX_SEARCH_ITERATIONS - 1:

                    st.warning(

                        "Reflection Agent decided to search again."

                    )

                    continue

                else:

                    st.warning(

                        "Reflection Agent could not find better jobs after multiple attempts."

                    )

                    break

            with st.spinner("Executing Decision..."):

                result = executor_agent(

                    decision,

                    profile,

                    ranked_jobs,

                    memory

                )

            st.success("Execution Completed")

            break
        if not ranked_jobs:

            st.error("No jobs found.")

            st.stop()

        show_jobs(ranked_jobs)

        best = ranked_jobs[0]

        show_best_job(best)

        if result is not None:

            action = result.get("action","")


            if action == "generate_cover_letter":

                memory["cover_letters_generated"] += 1

                st.markdown("---")

                st.header("✉ Generated Cover Letter")

                st.text_area(

                    "",

                    result["cover_letter"],

                    height=350

                )

                st.download_button(
                    "📥 Download Cover Letter",
                    result["cover_letter"],
                    file_name="cover_letter.txt"
                )

            elif action == "improve_resume":
                memory["resume_improvements"] += 1
                st.markdown("---")
                st.header("📄 Resume Suggestions")
                improvements = result["resume_improvements"]
                st.subheader("Missing Skills")
                for skill in improvements.get(
                    "missing_skills",
                    []
                ):

                    st.write("•",skill)

                st.subheader("Recommended Projects")

                for project in improvements.get(
                    "recommended_projects",
                    []
                ):

                    if isinstance(project,dict):

                        st.write(
                            f"• {project.get('title','')}"
                        )

                    else:

                        st.write("•",project)

                st.subheader("Resume Improvements")

                for item in improvements.get(
                    "resume_improvements",
                    []
                ):

                    if isinstance(item,dict):

                        st.write(
                            f"• {item.get('feedback','')}"
                        )

                    else:

                        st.write("•",item)

                st.subheader("ATS Keywords")

                st.write(

                    ", ".join(

                        improvements.get(
                            "ats_keywords",
                            []
                        )

                    )

                )

                st.subheader("Overall Feedback")

                st.info(

                    improvements.get(
                        "overall_feedback",
                        ""
                    )

                )



        st.markdown("---")

        st.header("🧠 Agent Memory")

        col1,col2,col3 = st.columns(3)

        with col1:

            st.metric(

                "Searches",

                memory["previous_searches"]

            )

        with col2:

            st.metric(

                "Cover Letters",

                memory["cover_letters_generated"]

            )

        with col3:

            st.metric(

                "Resume Improvements",

                memory["resume_improvements"]

            )

        if memory["history"]:

            st.markdown("---")

            st.header("📜 Agent History")

            for i,item in enumerate(memory["history"],1):

                st.write(

                    f"Iteration {i}:",

                    item["decision"]

                )

        st.success("🎉 Autonomous workflow completed.")     
