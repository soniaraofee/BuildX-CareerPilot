from career_agent import analyze_jobs


profile = {
    "name": "Sonia",
    "education": "Computer Engineering student",
    "skills": "Python, Git",
    "experience": "University projects",
    "target_role": "Backend Development",
    "work_type": "Remote",
}


jobs = [
    {
        "title": "Backend Developer Intern",
        "company": "TechNova",
        "requirements": ["Python", "Git"],
    }
]


result = analyze_jobs(
    profile,
    jobs
)


print(result)