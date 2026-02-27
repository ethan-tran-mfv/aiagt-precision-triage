"""
Response Builder Node [8/8]

Purpose:
  Construct the final API response from aggregated state.
  Last node in the graph — its output is what the user receives.

Input:  Full AgentState after aggregation
Output: state["metrics"]["response"] — the public API contract

Response schema (TDD §6.10):
  {
    "request_id":         string,
    "summary_posted":     bool,
    "tickets_created":    int,
    "duplicates_skipped": int,
    "slack_url":          string | null,
    "jira_urls":          list[string],
    "trace_id":           string,
    "errors":             list[dict]
  }

Teaching point:
  The response builder enforces the public API contract.
  It never exposes internal state — only the defined contract.
  Errors are surfaced structurally, not as exceptions.
"""

from schemas.state import AgentState


def response_builder_node(state: AgentState) -> AgentState:
    """
    [Node 8] Build the final API response from aggregated state.
    """
    # TODO: implement response builder node
    # Steps:
    #   1. slack_url  = state.get("slack_result", {}).get("slack_url")
    #   2. jira_urls  = [t["url"] for t in state.get("jira_result", {}).get("created", [])]
    #   3. Build response dict matching the schema above
    #   4. state["metrics"]["response"] = response
    #   5. Return state
    raise NotImplementedError
