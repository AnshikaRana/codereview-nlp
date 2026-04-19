import re


def extract_names(code):
    # Extract variable and function names from code
    functions = re.findall(r"def (\w+)", code)
    variables = re.findall(r"(\w+)\s*=", code)
    return functions + variables


def score_name(name):
    # Score a single name
    if len(name) <= 2:
        return 0
    if "_" in name or len(name) > 5:
        return 2
    return 1


# ✅ FINAL REQUIRED FUNCTION (PRD compliant)
def analyze_names(code: str) -> dict:
    names = extract_names(code)

    if not names:
        return {
            "module": "name_quality",
            "score": 100,
            "flags": [],
            "suggestions": []
        }

    flags = []
    suggestions = []
    scores = []

    for n in names:
        s = score_name(n)
        scores.append(s)

        if s == 0:
            flags.append(n)
            suggestions.append(f"rename '{n}' to something more descriptive")
        elif s == 1:
            flags.append(n)
            suggestions.append(f"consider improving clarity of '{n}'")

    # Normalize score to 0–100
    avg_score = sum(scores) / len(scores)   # between 0–2
    final_score = int((avg_score / 2) * 100)

    return {
        "module": "name_quality",
        "score": final_score,
        "flags": list(set(flags)),
        "suggestions": list(set(suggestions))
    }