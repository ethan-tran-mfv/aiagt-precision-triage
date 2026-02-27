"""
Response Builder Node [8/8]

Purpose:
  Construct the final API response from aggregated state.
  Adapts the response shape based on which agents were activated.

Response schema (TDD §6.12):
  {
    "request_id":         string,
    "intent":             string,
    "answer":             string | null,
    "summary_posted":     bool,
    "tickets_created":    int,
    "duplicates_skipped": int,
    "slack_url":          string | null,
    "jira_urls":          list[string],
    "issues_processed":   int,
    "issues_matched":     int,
    "trace_id":           string,
    "errors":             list[dict]
  }
"""

from schemas.state import AgentState


def response_builder_node(state: AgentState) -> AgentState:
    """
    [Node 8] Build the final API response from aggregated state.
    """
    # TODO: implement response builder node
    # Steps:
    #   1. intent         = state["enriched_task"]["intent"]
    #   2. answer         = state.get("answer_result", {}).get("answer")
    #   3. slack_url      = state.get("slack_result", {}).get("slack_url")
    #   4. summary_posted = state.get("slack_result", {}).get("success", False)
    #   5. jira_created   = state.get("jira_result", {}).get("created", [])
    #   6. jira_urls      = [t["url"] for t in jira_created if "url" in t]
    #   7. issues_matched = len(state.get("filtered_issues", []))
    #   8. issues_processed = len(state.get("parsed_issues", []))
    #   9. Build response dict from above
    #  10. state["metrics"]["response"] = response
    #  11. Return state
    raise NotImplementedError
