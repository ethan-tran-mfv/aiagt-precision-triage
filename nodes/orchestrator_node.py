"""
Orchestrator Node [6/8]

Purpose:
  Determine which agents to activate and generate a specialized query for each.
  Only activates agents the user actually requested.

Input:
  state["filtered_issues"]  issues ready for action
  state["enriched_task"]    task contract with agent activation flags

Output:
  state["slack_query"]   instruction for slack_agent  (if requires_slack_post)
  state["jira_query"]    instruction for jira_agent   (if requires_ticket_creation)
  state["answer_query"]  instruction for answer_agent (if requires_analysis)

Teaching point:
  The orchestrator is the bridge between "what the user wants" and "what each agent does."
  It generates a PURPOSE-BUILT query per agent — not generic instructions.

  Agent selection is DYNAMIC based on enriched_task flags:
    requires_slack_post       → activate Slack agent
    requires_ticket_creation  → activate JIRA agent
    requires_analysis         → activate Answer agent

  In the graph, only the activated agents run in parallel.
  Deactivated agents are skipped entirely (conditional edges).
"""

from schemas.state import AgentState


def orchestrator_node(state: AgentState) -> AgentState:
    """
    [Node 6] Generate sub-agent queries based on filtered issues and task contract.
    """
    # TODO: implement orchestrator node
    # Steps:
    #   1. issues      = state["filtered_issues"]
    #   2. task        = state["enriched_task"]
    #   3. criteria    = task.get("filter_criteria")
    #   4. issue_count = len(issues)
    #   5. issue_titles = ", ".join([i.get("title","") for i in issues[:5]])
    #   6. criteria_desc = criteria["description"] if criteria else "all QA issues"
    #
    #   7. If task["requires_slack_post"]:
    #        state["slack_query"] = _build_slack_query(
    #            issue_count, issue_titles, criteria_desc, task["output_format"]
    #        )
    #
    #   8. If task["requires_ticket_creation"]:
    #        state["jira_query"] = _build_jira_query(issue_count, criteria_desc)
    #
    #   9. If task["requires_analysis"]:
    #        state["answer_query"] = _build_answer_query(
    #            state["instruction"], issue_count, criteria_desc, task["output_format"]
    #        )
    #
    #   10. Return state
    raise NotImplementedError


def _build_slack_query(
    issue_count: int, issue_titles: str, criteria_desc: str, output_format: str
) -> str:
    """Build specialized instruction for Slack summary agent."""
    # TODO: return formatted instruction
    # Include: issue_count, issue_titles (sample), criteria_desc,
    # output_format (executive=<300 words / detailed=full breakdown / bullet=list),
    # focus on production risk and business impact
    raise NotImplementedError


def _build_jira_query(issue_count: int, criteria_desc: str) -> str:
    """Build specialized instruction for JIRA ticket creation agent."""
    # TODO: return formatted instruction
    # Include: issue_count, criteria_desc,
    # required ticket fields: summary, description, reproduction steps,
    # expected vs actual behavior, priority (P1/P2/P3)
    raise NotImplementedError


def _build_answer_query(
    original_instruction: str, issue_count: int, criteria_desc: str, output_format: str
) -> str:
    """Build specialized instruction for Answer agent analysis."""
    # TODO: return formatted instruction
    # Include: original_instruction, issue_count, criteria_desc,
    # output_format, ask for patterns, distribution, and recommendations
    raise NotImplementedError
