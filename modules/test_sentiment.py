from sentiment import analyze_sentiment

def test_all_positive():
    result = analyze_sentiment(["Great work!", "Clean and readable."])
    assert result["module"] == "review_tone"
    assert result["score"] == 100
    assert result["flags"] == []

def test_one_negative():
    result = analyze_sentiment(["This is wrong and terrible code."])
    assert result["score"] < 100
    assert len(result["flags"]) > 0

def test_aggressive_language():
    result = analyze_sentiment(["fix this now immediately!"])
    assert any("rephrase" in s for s in result["suggestions"])

def test_empty_list():
    result = analyze_sentiment([])
    assert result["score"] == 100

def test_return_keys():
    result = analyze_sentiment(["ok"])
    assert set(result.keys()) == {"module", "score", "flags", "suggestions"}

if __name__ == "__main__":
    test_all_positive()
    test_one_negative()
    test_aggressive_language()
    test_empty_list()
    test_return_keys()
    print("All sentiment tests passed.")