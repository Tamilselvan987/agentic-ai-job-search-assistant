from pypdf import PdfReader


def extract_resume_text(pdf_path):
    """
    Reads a PDF resume and returns its raw text.
    No AI reasoning happens here.
    """

    try:
        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text.strip()

    except Exception as e:
        print(f"Resume extraction failed: {e}")
        return ""
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def analyze_resume(resume_text):
    """
    Resume Analysis Agent

    Understands the candidate and creates
    a structured professional profile.
    """

    prompt = f"""
You are an expert technical recruiter.

Analyze the following resume.

Your task is to understand the candidate.

Return ONLY valid JSON.

The JSON format MUST be:

{{
    "supported": true,
    "confidence": 95,
    "resume_quality":"",
    "domain": "",
    "summary": "",
    "skills": [],
    "projects": [],
    "experience": [],
    "education": "",
    "preferred_roles": [],
    "reason": ""
}}

Rules

1. Decide whether this resume belongs to a software/IT professional.

2. If it is NOT software related:
   - supported = false
   - explain why

3. Determine the candidate's primary domain.

Examples:

Frontend Development

Backend Development

Full Stack Development

Mobile Development

AI / Machine Learning

Data Science

Cyber Security

Cloud / DevOps

UI/UX Design

4. Extract ONLY information actually present in the resume.

Return ALL keys listed in the JSON format.

If any information is missing, return:

summary: ""

skills: []

projects: []

experience: []

education: ""

preferred_roles: []

Do NOT omit any key.

Determine the candidate's preferred_roles based ONLY on information present in the resume.

Use these sources:

- Current and previous job titles
- Technical skills
- Professional summary
- Work experience

Examples

If the resume contains:

ReactJS, Next.js, HTML, CSS

Return:

preferred_roles:
[
    "Frontend Developer"
]

If the resume contains:

ReactJS, Node.js, Express

Return:

preferred_roles:
[
    "Full Stack Developer"
]

If the resume contains:

Flutter, Kotlin, Android

Return:

preferred_roles:
[
    "Mobile App Developer"
]

A candidate may have multiple preferred roles.

Only return roles that are clearly supported by the resume.

Do NOT invent skills.

Do NOT invent projects.

Do NOT invent education.

Do NOT invent experience.

Do NOT invent preferred roles that are not supported by the resume.

5. confidence must be between 0 and 100.

Determine the overall quality of the resume.

Return:

resume_quality

Possible values

"strong"

or

"weak"

A resume is considered weak if several important sections are missing or incomplete.

Examples

Weak Resume

- No projects
- Very few technical skills
- Poor professional summary
- No measurable achievements
- Very little experience

Strong Resume

- Good technical skills
- Relevant experience
- Well-written summary
- Strong achievements
- Projects or certifications
Resume

{resume_text}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "temperature": 0
        }
    )

    return json.loads(response.json()["response"])


def process_resume(pdf_path):
    text = extract_resume_text(pdf_path)
    return analyze_resume(text)