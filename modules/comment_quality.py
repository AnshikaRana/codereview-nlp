# modules/comment_quality.py
# P2 owns this file. Exports: analyze_comments(code: str) -> dict

import re
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# -----------------------------------
# Safe Java-dependent grammar checker
# -----------------------------------
try:
    import language_tool_python
    _tool = language_tool_python.LanguageTool('en-US')
    TOOL_AVAILABLE = True
except:
    _tool = None
    TOOL_AVAILABLE = False

# Load once at module level
_model = SentenceTransformer('all-MiniLM-L6-v2')

RESTATE_THRESHOLD = 0.82


def _extract_comment_code_pairs(code: str) -> list:
    pairs = []
    lines = code.splitlines()

    for i, line in enumerate(lines):
        stripped = line.strip()

        if '#' not in stripped:
            continue

        # Full line comment
        if stripped.startswith('#'):
            comment_text = stripped.lstrip('#').strip()
            next_code = ""

            for j in range(i + 1, min(i + 4, len(lines))):
                candidate = lines[j].strip()
                if candidate and not candidate.startswith('#'):
                    next_code = candidate
                    break

            pairs.append((comment_text, next_code))

        # Inline comment
        else:
            code_part, _, comment_part = line.partition('#')
            comment_text = comment_part.strip()
            code_context = code_part.strip()

            if comment_text:
                pairs.append((comment_text, code_context))

    return pairs


def _is_restatement(comment: str, code_context: str) -> bool:
    if not code_context:
        return False

    c_emb = _model.encode(comment, convert_to_tensor=True)
    k_emb = _model.encode(code_context, convert_to_tensor=True)

    similarity = cos_sim(c_emb, k_emb).item()
    return similarity > RESTATE_THRESHOLD


def analyze_comments(code: str) -> dict:
    flags = []
    suggestions = []

    pairs = _extract_comment_code_pairs(code)

    # No comments case
    if not pairs:
        if re.search(r'\bdef \w+', code):
            flags.append("no comments found in code with function definitions")
            suggestions.append(
                "add docstrings or inline comments explaining why, not what"
            )

        score = max(0, 100 - len(flags) * 15)

        return {
            "module": "comment_quality",
            "score": score,
            "flags": flags,
            "suggestions": suggestions
        }

    # Analyze each comment
    for comment, code_context in pairs:
        short_comment = comment[:50]

        # Too short comments
        if len(comment.strip()) < 6:
            flags.append(f"too sparse: '{short_comment}'")
            suggestions.append(
                "expand the comment — explain the reason, not just what"
            )
            continue

        # Grammar check only if Java available
        if TOOL_AVAILABLE:
            try:
                grammar_issues = _tool.check(comment)

                errors = [
                    i for i in grammar_issues
                    if i.rule_id not in (
                        "WHITESPACE_RULE",
                        "COMMA_PARENTHESIS_WHITESPACE"
                    )
                ]

                if len(errors) > 1:
                    flags.append(f"grammar issues: '{short_comment}'")
                    suggestions.append(
                        f"fix grammar in comment: '{short_comment}'"
                    )

            except:
                pass

        # Comment restates code
        if _is_restatement(comment, code_context):
            flags.append(f"restates code: '{short_comment}'")
            suggestions.append(
                "explain why this code exists, not just what it does"
            )

    score = max(0, 100 - len(flags) * 15)

    return {
        "module": "comment_quality",
        "score": score,
        "flags": list(set(flags)),
        "suggestions": list(set(suggestions))
    }