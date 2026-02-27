"""
End-to-end integration tests for the full AIA workflow.
Slack and JIRA are mocked. Requires Qdrant running + knowledge ingested.

  docker-compose up -d
  python rag/setup.py && python rag/ingest.py
  pytest tests/integration/test_end_to_end.py -v
"""

import uuid
import pytest
from unittest.mock import patch
from graph.workflow import build_graph
from schemas.state import AgentState


SAMPLE_CSV = (
    "id,title,description,steps,severity\n"
    "1,Revenue total incorrect,Dashboard shows $1200 but actual is $12000,Open dashboard,high\n"
    "2,Login button misaligned,Button is 5px off on mobile,,low\n"
    "3,Wrong user data shown,Profile shows another user's email,Log in,critical\n"
    "4,Search slow on large dataset,Takes 10 seconds,,medium\n"
    "5,ML model wrong label,Fraud transaction classified as legitimate,Submit transaction,high\n"
)


@pytest.fixture(scope="module")
def graph():
    return build_graph()


def base_state() -> AgentState:
    return {
        "request_id": str(uuid.uuid4()), "trace_id": str(uuid.uuid4()),
        "instruction": "Summarize accuracy issues and create JIRA tickets",
        "raw_file_content": SAMPLE_CSV, "file_name": "test_issues.csv",
        "enriched_task": None, "accuracy_definition": None, "parsed_issues": [],
        "classified_issues": [], "accuracy_issues": [], "slack_query": None,
        "jira_query": None, "slack_result": None, "jira_result": None,
        "errors": [], "metrics": {},
    }


@patch("agents.slack_agent.SlackAgent.run")
@patch("agents.jira_agent.JiraAgent.run")
def test_full_workflow_happy_path(mock_jira, mock_slack, graph):
    mock_slack.return_value = {
        "summary_markdown": "## 3 accuracy issues found.",
        "slack_url": "https://slack.com/msg/123",
        "success": True, "error": None,
    }
    mock_jira.return_value = {
        "created": [{"issue_id": "1", "url": "https://jira.example.com/AIA-1"}],
        "duplicates": [], "success": True, "error": None,
    }
    final = graph.invoke(base_state())
    response = final["metrics"]["response"]
    assert response["summary_posted"] is True
    assert response["tickets_created"] >= 1
    assert len(final["accuracy_issues"]) >= 1


@patch("agents.slack_agent.SlackAgent.run")
@patch("agents.jira_agent.JiraAgent.run")
def test_slack_failure_does_not_block_jira(mock_jira, mock_slack, graph):
    mock_slack.return_value = {
        "summary_markdown": "", "slack_url": None,
        "success": False, "error": "Rate limited",
    }
    mock_jira.return_value = {
        "created": [{"issue_id": "1", "url": "https://jira.example.com/AIA-1"}],
        "duplicates": [], "success": True, "error": None,
    }
    final = graph.invoke(base_state())
    response = final["metrics"]["response"]
    assert response["summary_posted"] is False
    assert response["tickets_created"] >= 1
