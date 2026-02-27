"""
Filter Node [5/8]

Purpose:
  Two modes depending on whether classification was performed:

  Mode A — with filter_criteria (classification was run):
    Keep issues where matches_criteria == True AND confidence >= threshold

  Mode B — without filter_criteria (classification skipped):
    Pass ALL parsed_issues through as filtered_issues unchanged

Output:
  state["filtered_issues"]  ready for orchestrator

Teaching point:
  The threshold is set dynamically by the enrichment node.
  If the user said "strict" → 0.8. If "all" → 0.4. Default → 0.6.

  Lab exercise: change threshold and observe precision vs recall in Langfuse.
"""

from schemas.state import AgentState


def filter_node(state: AgentState) -> AgentState:
    """
    [Node 5] Filter issues by criteria match and confidence threshold.
    Falls back to pass-through when no filter_criteria is set.
    """
    # TODO: implement filter node
    # Steps:
    #   1. criteria = state["enriched_task"].get("filter_criteria")
    #
    #   2. Mode A — filter_criteria is NOT None (classification was run):
    #        threshold = criteria["confidence_threshold"]
    #        state["filtered_issues"] = [
    #            i for i in state["classified_issues"]
    #            if i["matches_criteria"] and i["confidence"] >= threshold
    #        ]
    #
    #   3. Mode B — filter_criteria is None (no classification):
    #        state["filtered_issues"] = state["parsed_issues"]  # pass all through
    #
    #   4. If filtered_issues is empty:
    #        state["metrics"]["early_exit"] = True
    #        state["metrics"]["early_exit_reason"] = "No issues matched the criteria"
    #
    #   5. Return state
    raise NotImplementedError
