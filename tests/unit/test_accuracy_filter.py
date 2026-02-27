"""Unit tests for filter_node — threshold logic."""

import pytest
from nodes.filter_node import filter_node
from schemas.state import AgentState


def make_state(classified_issues: list, threshold: float) -> AgentState:
    return {
        "request_id": "test-001", "trace_id": "trace-001",
        "instruction": "", "raw_file_content": "", "file_name": "",
        "enriched_task": {
            "task_type": "accuracy_filter",
            "requires_slack_post": True,
            "requires_ticket_creation": True,
            "confidence_threshold": threshold,
        },
        "accuracy_definition": None, "parsed_issues": [],
        "classified_issues": classified_issues, "accuracy_issues": [],
        "slack_query": None, "jira_query": None, "slack_result": None,
        "jira_result": None, "errors": [], "metrics": {},
    }


SAMPLE = [
    {"issue_id": "1", "accuracy_related": True,  "confidence": 0.90, "reason": "Wrong calc"},
    {"issue_id": "2", "accuracy_related": True,  "confidence": 0.55, "reason": "Possible"},
    {"issue_id": "3", "accuracy_related": False, "confidence": 0.80, "reason": "UI bug"},
    {"issue_id": "4", "accuracy_related": True,  "confidence": 0.70, "reason": "Wrong data"},
]


def test_filter_default_threshold():
    result = filter_node(make_state(SAMPLE, threshold=0.6))
    ids = [i["issue_id"] for i in result["accuracy_issues"]]
    assert "1" in ids and "4" in ids
    assert "2" not in ids and "3" not in ids


def test_filter_strict_threshold():
    result = filter_node(make_state(SAMPLE, threshold=0.8))
    ids = [i["issue_id"] for i in result["accuracy_issues"]]
    assert ids == ["1"]


def test_filter_lenient_threshold():
    result = filter_node(make_state(SAMPLE, threshold=0.4))
    ids = [i["issue_id"] for i in result["accuracy_issues"]]
    assert set(ids) == {"1", "2", "4"}


def test_empty_result_sets_early_exit_flag():
    result = filter_node(make_state(SAMPLE, threshold=0.99))
    assert result["accuracy_issues"] == []
    assert result["metrics"].get("early_exit") is True
