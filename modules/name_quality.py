import re

# Common valid engineering names
VALID_NAMES = {
    "user", "users", "token", "app", "data", "result",
    "index", "count", "config", "email", "url",
    "response", "request", "payload", "items",
    "name", "value", "message", "file", "path",
    "hours", "minutes", "seconds", "price", "tax",
    "customer", "profile", "status", "role",
    "list", "dict", "set", "obj", "row", "col"
}

# Weak / unclear names
BAD_NAMES = {
    "x", "y", "z", "a", "b", "c",
    "u", "p", "i", "j", "k",
    "tmp", "temp", "var", "abc",
    "foo", "bar"
}


def extract_names(code):
    # Extract function names
    functions = re.findall(r"def\s+([a-zA-Z_]\w*)", code)

    # Extract variable names
    variables = re.findall(r"\b([a-zA-Z_]\w*)\s*=", code)

    return functions + variables


def is_descriptive(name):
    # snake_case names
    if "_" in name and len(name) >= 5:
        return True

    # camelCase names
    if re.search(r"[a-z][A-Z]", name) and len(name) >= 5:
        return True

    # Long readable words
    if len(name) >= 6:
        return True

    return False


def score_name(name):
    lower = name.lower()

    # Clearly valid names
    if lower in VALID_NAMES:
        return 2

    # Clearly weak names
    if lower in BAD_NAMES:
        return 0

    # Too short
    if len(name) <= 2:
        return 0

    # Descriptive structure
    if is_descriptive(name):
        return 2

    # Medium quality
    if len(name) <= 4:
        return 1

    return 2


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