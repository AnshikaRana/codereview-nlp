"""
modules/sentiment.py
P3 owns this file. Exports: analyze_sentiment(review_comments: list) -> dict
"""
from transformers import pipeline

_pipe = pipeline('sentiment-analysis', model='cardiffnlp/twitter-roberta-base-sentiment')

AGGRESSIVE = ['wrong', 'bad', 'terrible', 'why would', 'did you even', 'immediately', 'fix this now']

def analyze_sentiment(review_comments: list) -> dict:
    flags, suggestions = [], []
    neg_count = 0

    for c in review_comments:
        if not c or not c.strip():
            continue
        result = _pipe(c[:512])[0]
        if result['label'] == 'LABEL_0':
            neg_count += 1
            flags.append(f'negative tone: {c[:50]}')
            if any(w in c.lower() for w in AGGRESSIVE):
                suggestions.append(f'rephrase constructively: {c[:40]}')

    score = max(0, 100 - neg_count * 20)

    return {
        "module": "review_tone",
        "score": int(score),
        "flags": flags,
        "suggestions": suggestions
    }