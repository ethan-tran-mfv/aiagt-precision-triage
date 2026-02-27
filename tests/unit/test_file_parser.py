"""Unit tests for file_parser_node."""

import pytest
from nodes.file_parser_node import file_parser_node
from schemas.state import AgentState


def make_state(file_name: str, content: str) -> AgentState:
    return {
        "request_id": "test-001", "trace_id": "trace-001",
        "instruction": "", "raw_file_content": content, "file_name": file_name,
        "enriched_task": None, "accuracy_definition": None, "parsed_issues": [],
        "classified_issues": [], "accuracy_issues": [], "slack_query": None,
        "jira_query": None, "slack_result": None, "jira_result": None,
        "errors": [], "metrics": {},
    }


def test_parse_csv_returns_issues():
    csv_content = "id,title,description,steps,severity\n1,Bug A,Wrong total,,high"
    result = file_parser_node(make_state("issues.csv", csv_content))
    assert len(result["parsed_issues"]) == 1
    assert result["parsed_issues"][0]["title"] == "Bug A"


def test_parse_csv_missing_required_field_raises():
    csv_content = "title,description\nBug A,Wrong total"  # missing 'id'
    with pytest.raises((ValueError, KeyError)):
        file_parser_node(make_state("issues.csv", csv_content))


def test_parse_csv_fills_optional_fields():
    csv_content = "id,title,description\n1,Bug A,Wrong total"
    result = file_parser_node(make_state("issues.csv", csv_content))
    assert result["parsed_issues"][0]["steps"] == ""
    assert result["parsed_issues"][0]["severity"] == ""


def test_unsupported_format_raises():
    with pytest.raises(ValueError):
        file_parser_node(make_state("issues.pdf", "content"))
