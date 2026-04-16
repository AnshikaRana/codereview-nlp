import re


def extract_names(code):
    # Extract variable and function names from code
    # function names
    functions = re.findall(r"def (\w+)", code)

    # variable names (simple version)
    variables = re.findall(r"(\w+)\s*=", code)

    return functions + variables


def score_name(name):
    
    # Score a single name
    # very short names → bad
    if len(name) <= 2:
        return 0

    # meaningful names (has underscore or readable words)
    if "_" in name or len(name) > 5:
        return 2

    return 1


def name_quality_score(code):

    # Final score for a code snippet    
    names = extract_names(code)

    if not names:
        return 1  # neutral

    scores = [score_name(n) for n in names]

    return sum(scores) / len(scores)