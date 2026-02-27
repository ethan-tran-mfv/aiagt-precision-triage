"""
Orchestrator Node [6/8]

Purpose:
  Generate specialized queries for each sub-agent.
  Decides which agents to activate and what to tell each one.

Input:
  state["accuracy_issues"]  filtered issues ready for action
  state["enriched_task"]    task contract (requires_slack_post / requires_ticket_creation)

Output:
  state["slack_query"]   purpose-built instruction for slack_agent  (or None)
  state["jira_query"]    purpose-built instruction for jira_agent   (or None)

Teaching point:
  The orchestrator is the bridge between intent and execution.
  It never passes raw user input to sub-agents.
  Each sub-agent receives a query tailored to its specific job.

  Raw intent → Enrichment → Contract → Orchestrator → Specialized queries
                                                              ↓          ↓
                                                        slack_agent  jira_agent
"""

from schemas.state import AgentState


def orchestrator_node(state: AgentState) -> AgentState:
    """
    [Node 6] Generate sub-agent queries from filtered issues and task contract.
    """
    # TODO: implement orchestrator node
    # Steps:
    #   1. issues      = state["accuracy_issues"]
    #   2. task        = state["enriched_task"]
    #   3. issue_count = len(issues)
    #   4. issue_titles = ", ".join([i["title"] for i in issues[:5]])
    #
    #   5. If task["requires_slack_post"]:
    #        state["slack_query"] = _build_slack_query(issue_count, issue_titles)
    #
    #   6. If task["requires_ticket_creation"]:
    #        state["jira_query"]  = _build_jira_query(issue_count)
    #
    #   7. Return state
    raise NotImplementedError


def _build_slack_query(issue_count: int, issue_titles: str) -> str:
    """
    Build a specialized instruction for the Slack summary agent.
    Focus: executive communication, production risk, markdown, ≤300 words.
    """
    # TODO: return formatted instruction string for Slack agent
    raise NotImplementedError


def _build_jira_query(issue_count: int) -> str:
    """
    Build a specialized instruction for the JIRA ticket creation agent.
    Focus: structured format, priority P1/P2/P3, reproduction steps.
    """
    # TODO: return formatted instruction string for JIRA agent
    raise NotImplementedError
