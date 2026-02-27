"""
Aggregator Node [7/8]

Purpose:
  Merge results from both parallel branches (Slack + JIRA) into unified state.
  Handles partial failures — one branch failing does not nullify the other.

Input:
  state["slack_result"]  SlackResult (may contain error field)
  state["jira_result"]   JiraResult  (may contain error field)

Output:
  state["metrics"]  updated with ticket counts, duplicate rate, success flags

Teaching point:
  Parallel branches converge here. The aggregator must handle all combinations:
    ✓ Both success      ✓ Slack fail + JIRA success
    ✓ Both fail         ✓ Slack success + JIRA fail
  Failure isolation = the system always returns a meaningful partial response.
"""

from schemas.state import AgentState


def aggregator_node(state: AgentState) -> AgentState:
    """
    [Node 7] Merge Slack and JIRA branch results into unified metrics.
    """
    # TODO: implement aggregator node
    # Steps:
    #   1. slack = state.get("slack_result") or {}
    #   2. jira  = state.get("jira_result")  or {}
    #   3. tickets_created    = len(jira.get("created", []))
    #   4. duplicates_skipped = len(jira.get("duplicates", []))
    #   5. total              = tickets_created + duplicates_skipped
    #   6. duplicate_rate     = duplicates_skipped / total if total > 0 else 0
    #   7. Merge into state["metrics"]:
    #        tickets_created, duplicates_skipped, duplicate_rate,
    #        slack_success, jira_success
    #   8. Return state
    raise NotImplementedError
