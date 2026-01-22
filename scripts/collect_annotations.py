import os, requests, csv

TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["REPO"]
RUN_ID = os.environ["RUN_ID"]

API = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()

# Get check suites for the run
suites = get(f"{API}/repos/{REPO}/actions/runs/{RUN_ID}/check-suites")

rows = []

for suite in suites["check_suites"]:
    runs = get(f"{API}/repos/{REPO}/check-suites/{suite['id']}/check-runs")

    for run in runs["check_runs"]:
        page = 1
        while True:
            anns = get(
                f"{API}/repos/{REPO}/check-runs/{run['id']}/annotations",
                params={"per_page": 100, "page": page}
            )
            if not anns:
                break

            for a in anns:
                rows.append([
                    run["name"],                 # check name
                    a["annotation_level"],       # warning / failure
                    a["path"],                   # file
                    a["start_line"],             # start line
                    a["end_line"],               # end line
                    a["message"]                 # message
                ])
            page += 1

# Save CSV
os.makedirs("reports", exist_ok=True)
csv_path = "reports/analysis_report.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "check_name",
        "severity",
        "file_path",
        "line_start",
        "line_end",
        "message"
    ])
    writer.writerows(rows)

print(f"Saved {len(rows)} findings to {csv_path}")
