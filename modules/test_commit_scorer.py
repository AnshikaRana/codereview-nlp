from commit_scorer import score_commit

def test_perfect_commit():
    result = score_commit("Add user authentication module")
    assert result["score"] == 100
    assert result["flags"] == []

def test_no_imperative():
    result = score_commit("added some stuff")
    assert "does not start with imperative verb" in result["flags"]

def test_too_long():
    result = score_commit("Fix " + "a" * 80)
    assert "commit message too long (>72 chars)" in result["flags"]

def test_vague():
    result = score_commit("update changes misc wip")
    assert "commit message is vague" in result["flags"]

def test_return_keys():
    result = score_commit("Fix bug")
    assert set(result.keys()) == {"module", "score", "flags", "suggestions"}
    assert result["module"] == "commit_quality"

if __name__ == "__main__":
    test_perfect_commit()
    test_no_imperative()
    test_too_long()
    test_vague()
    test_return_keys()
    print("All commit scorer tests passed.")