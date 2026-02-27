"""
Filter Node [5/8]

Purpose:
  Retain only accuracy-related issues that meet the confidence threshold.
  Pure logic — no LLM, no external calls.

Input:
  state["classified_issues"]  list of ClassifiedIssue
  state["enriched_task"]      contains confidence_threshold

Output:
  state["accuracy_issues"]    filtered subset

Filter logic:
  include if: accuracy_related == True AND confidence >= confidence_threshold

Teaching point:
  The threshold is set dynamically by the enrichment node — not hardcoded.
  Lab exercise: set threshold=0.9 vs threshold=0.4 and observe the
  precision vs recall tradeoff in Langfuse metrics.
"""

from schemas.state import AgentState


def filter_node(state: AgentState) -> AgentState:
    """
    [Node 5] Filter classified issues by accuracy flag and confidence threshold.
    """
    # TODO: implement filter node
    # Steps:
    #   1. threshold = state["enriched_task"]["confidence_threshold"]
    #   2. Filter state["classified_issues"]:
    #        keep where accuracy_related == True AND confidence >= threshold
    #   3. state["accuracy_issues"] = filtered list
    #   4. If accuracy_issues is empty:
    #        state["metrics"]["early_exit"] = True
    #        (graph-level conditional edge handles short-circuit)
    #   5. Return state
    raise NotImplementedError
