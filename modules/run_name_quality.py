import json
from name_quality import name_quality_score

# Load dataset
with open("data/prs.json", "r") as f:
    data = json.load(f)

results = []

for item in data:
    code = item.get("code", "")
    score = name_quality_score(code)

    results.append({
        "commit_msg": item.get("commit_msg", ""),
        "score": round(score, 2),
        "length_of_code": len(code)
    })

# Save results
with open("data/name_scores.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Processed {len(results)} PRs")