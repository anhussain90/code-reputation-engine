import os
import requests

TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["REPO"]
API = "https://api.github.com"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Find workflow id by name
workflows = requests.get(
    f"{API}/repos/{REPO}/actions/workflows",
    headers=headers
).json()["workflows"]

analysis_wf = next(w for w in workflows if w["name"] == "Static Analysis")

runs = requests.get(
    f"{API}/repos/{REPO}/actions/workflows/{analysis_wf['id']}/runs",
    headers=headers,
    params={"per_page": 1}
).json()["workflow_runs"]

latest_run_id = runs[0]["id"]

print(f"Latest run id: {latest_run_id}")

# Export as workflow output
with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"run_id={latest_run_id}\n")
