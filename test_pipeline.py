from modules.name_quality import analyze_names
from modules.comment_quality import analyze_comments
from modules.commit_scorer import score_commit
from modules.sentiment import analyze_sentiment

TEST_CODE = "def d(x,y):\n # calc\n return x+y"
TEST_MSG = "fix stuff"
TEST_REVS = ["this is terrible", "change this immediately"]

results = [
    analyze_names(TEST_CODE),
    analyze_comments(TEST_CODE),
    score_commit(TEST_MSG),
    analyze_sentiment(TEST_REVS)
]

for r in results:
    assert isinstance(r["score"], int)
    assert 0 <= r["score"] <= 100
    assert isinstance(r["flags"], list)
    assert isinstance(r["suggestions"], list)
    print(r)

print("✅ FULL PIPELINE WORKS")