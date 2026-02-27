"""Unit tests for filter_node — supports both filter modes."""

import pytest
from nodes.filter_node import filter_node
from schemas.state import AgentState


def make_state(classified_issues: list, threshold: float, has_criteria: bool = True) -> AgentState:
    return {
        "request_id": "test-001", "trace_id": "trace-001",
        "instruction": "", "raw_file_content": None, "file_name": None,
        "enriched_task": {
            "intent": "filter_and_report",
            "requires_file_processing": True,
            "filter_criteria": {
                "type": "accuracy",
                "description": "Issues involving incorrect outputs or wrong calculations",
                "confidence_threshold": threshold,
            } if has_criteria else None,
            "requires_slack_post": True,
            "requires_ticket_creation": True,
            "requires_analysis": False,
            "output_format": "executive",
        },
        "rag_context": None, "parsed_issues": [],
        "classified_issues": classified_issues, "filtered_issues": [],
        "slack_query": None, "jira_query": None, "answer_query": None,
        "slack_result": None, "jira_result": None, "answer_result": None,
        "errors": [], "metrics": {},
    }


SAMPLE = [
    {"issue_id": "1", "matches_criteria": True,  "confidence": 0.90, "reason": "Wrong calc"},
    {"issue_id": "2", "matches_criteria": True,  "confidence": 0.55, "reason": "Possible"},
    {"issue_id": "3", "matches_criteria": False, "confidence": 0.80, "reason": "UI bug"},
    {"issue_id": "4", "matches_criteria": True,  "confidence": 0.70, "reason": "Wrong data"},
]

PARSED = [
    {"id": "1", "title": "Bug A", "description": "...", "steps": "", "severity": "high"},
    {"id": "2", "title": "Bug B", "description": "...", "steps": "", "severity": "low"},
]


def test_filter_with_criteria_default_threshold():
    result = filter_node(make_state(SAMPLE, threshold=0.6))
    ids = [i["issue_id"] for i in result["filtered_issues"]]
    assert "1" in ids and "4" in ids
    assert "2" not in ids and "3" not in ids


def test_filter_with_criteria_strict_threshold():
    result = filter_node(make_state(SAMPLE, threshold=0.8))
    assert [i["issue_id"] for i in result["filtered_issues"]] == ["1"]


def test_filter_without_criteria_passes_all_parsed_issues():
    """Mode B: no filter_criteria → pass all parsed_issues through."""
    state = make_state([], threshold=0.6, has_criteria=False)
    state["parsed_issues"] = PARSED
    result = filter_node(state)
    assert len(result["filtered_issues"]) == 2


def test_empty_result_sets_early_exit_flag():
    result = filter_node(make_state(SAMPLE, threshold=0.99))
    assert result["filtered_issues"] == []
    assert result["metrics"].get("early_exit") is True
