from jobs import load_jobs, filter_jobs_by_role


jobs = load_jobs()

backend_jobs = filter_jobs_by_role(
    jobs,
    "Backend Development"
)

print("Backend opportunities:")
print()

for job in backend_jobs:
    print(
        f"- {job['title']} | {job['company']}"
    )