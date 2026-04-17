"""
modules/commit_scorer.py
P3 owns this file. Exports: score_commit(commit_msg: str) -> dict
"""
IMPERATIVE = ['add', 'fix', 'update', 'refactor', 'remove', 'implement',
              'improve', 'resolve', 'bump', 'create']
VAGUE = ['fix stuff', 'minor', 'update', 'changes', 'misc', 'wip',
         'temp', 'test', 'stuff', 'ok']

def score_commit(commit_msg: str) -> dict:
    msg = commit_msg.strip().lower()
    score, flags, suggestions = 0, [], []

    if not msg:
        return {
            "module": "commit_quality",
            "score": 0,
            "flags": ["empty commit message"],
            "suggestions": ["write a meaningful commit message"]
        }

    first_word = msg.split()[0]

    if first_word in IMPERATIVE:
        score += 34
    else:
        flags.append('does not start with imperative verb')
        suggestions.append('start with Add / Fix / Refactor etc.')

    if len(msg) <= 72:
        score += 33
    else:
        flags.append('commit message too long (>72 chars)')

    if not any(v in msg for v in VAGUE):
        score += 33
    else:
        flags.append('commit message is vague')
        suggestions.append('be specific about what changed')

    return {
        "module": "commit_quality",
        "score": int(score),
        "flags": flags,
        "suggestions": suggestions
    }