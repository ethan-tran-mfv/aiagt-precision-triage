"""Unit tests for ClassifiedIssue schema validation."""


def validate_classified_issue(issue: dict) -> bool:
    required = {"issue_id", "accuracy_related", "confidence", "reason"}
    if not required.issubset(issue.keys()):
        return False
    if not isinstance(issue["accuracy_related"], bool):
        return False
    if not (0.0 <= issue["confidence"] <= 1.0):
        return False
    if issue["accuracy_related"] and not issue["reason"]:
        return False
    return True


def test_valid_accuracy_issue():
    assert validate_classified_issue({
        "issue_id": "1", "accuracy_related": True,
        "confidence": 0.85, "reason": "Incorrect numerical output",
    }) is True


def test_valid_non_accuracy_issue():
    assert validate_classified_issue({
        "issue_id": "2", "accuracy_related": False,
        "confidence": 0.20, "reason": "UI layout problem",
    }) is True


def test_missing_reason_for_accuracy_issue_fails():
    assert validate_classified_issue({
        "issue_id": "3", "accuracy_related": True,
        "confidence": 0.80, "reason": "",
    }) is False


def test_confidence_out_of_range_fails():
    assert validate_classified_issue({
        "issue_id": "4", "accuracy_related": True,
        "confidence": 1.5, "reason": "Some reason",
    }) is False


def test_missing_required_key_fails():
    assert validate_classified_issue({
        "accuracy_related": True, "confidence": 0.9, "reason": "Some reason",
    }) is False
