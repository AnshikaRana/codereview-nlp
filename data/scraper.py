import requests
import json
import os

# Get token safely
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {TOKEN}"
}

# Optional debug (remove later)
print("Token loaded:", TOKEN is not None)

data = []

#Loop through pages (7 pages ≈ 210 PRs)
for page in range(1, 8):
    print(f"Fetching page {page}...")

    url = f"https://api.github.com/repos/pallets/flask/pulls?state=closed&per_page=30&page={page}"

    response = requests.get(url, headers=headers)

    # Check API success
    if response.status_code != 200:
        print("API Error:", response.status_code)
        print(response.text)
        break

    prs = response.json()

    # Safety check
    if not isinstance(prs, list):
        print("Unexpected response:", prs)
        break

    for pr in prs:
        try:
            entry = {
                "code": "dummy code",
                "inline_comments": [],
                "commit_msg": pr.get("title", ""),
                "review_comments": []
            }
            data.append(entry)
        except Exception as e:
            print("Error processing PR:", e)

# Save data (clean overwrite)
file_path = "data/prs.json"

with open(file_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"\n Total PRs saved: {len(data)}")