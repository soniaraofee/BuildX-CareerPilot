import json
from pathlib import Path


def load_jobs():
    file_path = Path(__file__).parent / "data" / "jobs.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def filter_jobs_by_role(jobs, target_role):

    role_keywords = {
        "Backend Development": [
            "Backend",
            "Python",
        ],
        "Frontend Development": [
            "Frontend",
        ],
        "Data Analysis": [
            "Data",
        ],
        "AI / Machine Learning": [
            "AI",
            "ML",
        ],
        "C++ / Software Development": [
            "C++",
            "Software",
        ],
    }

    keywords = role_keywords.get(target_role, [])

    filtered_jobs = []

    for job in jobs:

        text = (
            job["title"]
            + " "
            + job["description"]
        )

        if any(
            keyword.lower() in text.lower()
            for keyword in keywords
        ):
            filtered_jobs.append(job)

    return filtered_jobs