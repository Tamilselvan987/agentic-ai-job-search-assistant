from tools.job_tool import fetch_jobs

jobs = fetch_jobs()

print(f"Total Jobs: {len(jobs)}")

print()

for job in jobs[:5]:
    print(job["title"])
    print(job["company"])
    print(job["source"])
    print(job["url"])
    print("-----------------------")