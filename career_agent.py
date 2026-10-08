from unittest import result

from pydantic import BaseModel
from agent import ask_agent


class JobAnalysis(BaseModel):
    title: str
    company: str
    match_score: int
    why: str
    missing_skills: list[str]


class CareerAnalysis(BaseModel):
    jobs: list[JobAnalysis]
    top_recommendation: str
    action_tip: str

class ApplicationPreparation(BaseModel):
    summary: str
    strengths: list[str]
    focus_areas: list[str]

def analyze_jobs(profile, jobs):

    prompt = f"""
You are CareerPilot, an AI career assistant.

Analyze the available job opportunities for this candidate.

Candidate profile:
Name: {profile["name"]}
Education: {profile["education"]}
Skills: {profile["skills"]}
Experience: {profile["experience"]}
Resume: {profile["resume"]}
Target role: {profile["target_role"]}
Preferred work type: {profile["work_type"]}

Available opportunities:
{jobs}

For every opportunity:
- Give a match score from 0 to 100.
- Explain why it matches the candidate.
- List the most important missing skills.

Then:
- Select the best opportunity.
- Give one practical action tip for the candidate.

IMPORTANT:
Return ONLY valid JSON.
Do not use Markdown.
Do not add explanations outside the JSON.

Use exactly this structure:

{{
    "jobs": [
        {{
            "title": "Job title",
            "company": "Company name",
            "match_score": 85,
            "why": "Explanation",
            "missing_skills": ["SQL", "Django"]
        }}
    ],
    "top_recommendation": "Job title - Company",
    "action_tip": "Practical advice"
}}
"""

    result = ask_agent(prompt)

    return CareerAnalysis.model_validate_json(result)

def refine_recommendations(profile, jobs, current_analysis, feedback):
    prompt = f"""
You are CareerPilot, an AI career assistant.

The candidate has reviewed the previous recommendations and provided feedback.

Candidate profile:
Name: {profile["name"]}
Education: {profile["education"]}
Skills: {profile["skills"]}
Experience: {profile["experience"]}
Resume:
{profile["resume"]}
Original target role: {profile["target_role"]}
Original preferred work type: {profile["work_type"]}

Previous recommendations:
{current_analysis.model_dump_json()}

Candidate feedback:
{feedback}

Available opportunities:
{jobs}

Your task is to refine the recommendations based on the candidate's feedback.

Rules:
- Treat the feedback as a new preference that can change the ranking.
- Reconsider the available opportunities instead of blindly keeping the previous ranking.
- You may select a different job if the feedback makes it a better fit.
- Consider work type and role preferences mentioned in the feedback.
- Use ONLY the provided jobs.
- Do not invent jobs, requirements, skills, or candidate experience.
- Give a new match score from 0 to 100.
- Explain how the feedback affected the recommendation.
- Update the action tip based on the refined recommendation.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "jobs": [
        {{
            "title": "Job title",
            "company": "Company name",
            "match_score": 85,
            "why": "Explanation of the refined match",
            "missing_skills": ["SQL", "Django"]
        }}
    ],
    "top_recommendation": "Job title - Company",
    "action_tip": "Practical advice based on the refined recommendation"
}}
"""

    result = ask_agent(prompt)

    return CareerAnalysis.model_validate_json(result)
class ResumeImprovement(BaseModel):
    improved_summary: str
    highlighted_skills: list[str]
    suggested_changes: list[str]

def improve_resume(profile, feedback):
    prompt = f"""
You are CareerPilot, an AI career assistant.

Improve the candidate's resume focus based on the candidate's feedback.

Candidate profile:
Name: {profile["name"]}
Education: {profile["education"]}
Skills: {profile["skills"]}
Experience: {profile["experience"]}
Current resume:
{profile["resume"]}
Target role: {profile["target_role"]}

Candidate feedback:
{feedback}

Your task:
- Create an improved professional summary based ONLY on the provided information.
- Identify the most relevant existing skills that should be highlighted.
- Suggest practical changes to improve the resume.
- Do not invent work experience, projects, skills, achievements, or technologies.
- Do not claim the candidate has a skill that is not present in the profile.
- Keep the summary concise and professional.

Return ONLY valid JSON.

The JSON object MUST contain these EXACT keys:
- improved_summary
- highlighted_skills
- suggested_changes

Do not rename, remove, or add keys.

Example:

{
    "improved_summary": "Computer Engineering student with experience in Python, Git, and Linux, seeking opportunities in backend development.",
    "highlighted_skills": [
        "Python",
        "Git",
        "Linux"
    ],
    "suggested_changes": [
        "Emphasize Python projects relevant to backend development.",
        "Highlight practical Linux experience.",
        "Place the most relevant technical skills near the top of the resume."
    ]
}
"""

    result = ask_agent(prompt)

    return ResumeImprovement.model_validate_json(result)
def generate_application(profile, job):

    prompt = f"""
You are CareerPilot, an AI career assistant.

Create a concise application preparation summary for this candidate and job.

Candidate:
Name: {profile["name"]}
Education: {profile["education"]}
Skills: {profile["skills"]}
Experience: {profile["experience"]}
Resume: {profile["resume"]}

Selected job:
Title: {job["title"]}
Company: {job["company"]}
Description: {job["description"]}
Requirements: {job["requirements"]}

Create:
1. A short professional summary tailored to this job.
2. Three candidate strengths relevant to the job.
3. Three skills or areas the candidate should emphasize or improve.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "Short professional summary",
    "strengths": [
        "Strength 1",
        "Strength 2",
        "Strength 3"
    ],
    "focus_areas": [
        "Focus area 1",
        "Focus area 2",
        "Focus area 3"
    ]
}}
"""

    result = ask_agent(prompt)

    return ApplicationPreparation.model_validate_json(result)