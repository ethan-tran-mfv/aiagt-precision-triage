"""
LangGraph Workflow — QA Intelligence Agent (QAIA)

This file is the single source of truth for the system's execution.
Reading build_graph() tells you everything about how the system runs.

Routing decisions (conditional edges):

  [1] After enrichment:
      requires_file_processing == False → jump directly to answer_branch
      requires_file_processing == True  → proceed to rag_node

  [2] After rag_node + file_parser:
      filter_criteria is None → skip classification, go straight to filter
      filter_criteria set     → run classification

  [3] After filter_node:
      filtered_issues is empty → early_exit to response_builder
      filtered_issues not empty → proceed to orchestrator

  [4] After orchestrator (parallel fan-out — all active agents run concurrently):
      requires_slack_post       → run slack_branch
      requires_ticket_creation  → run jira_branch
      requires_analysis         → run answer_branch
      (inactive branches are skipped)

Teaching point:
  Every add_conditional_edges() call teaches a routing concept:
    - Intent routing (query vs file processing)
    - Conditional processing (with/without filter criteria)
    - Early exit (short-circuit when no results)
    - Dynamic agent activation (run only what's needed)
"""

from langgraph.graph import StateGraph, END
from schemas.state import AgentState

from nodes.enrichment_node import enrichment_node
from nodes.rag_node import rag_node
from nodes.file_parser_node import file_parser_node
from nodes.classification_node import classification_node
from nodes.filter_node import filter_node
from nodes.orchestrator_node import orchestrator_node
from nodes.aggregator_node import aggregator_node
from nodes.response_builder_node import response_builder_node

from agents.slack_agent import slack_agent
from agents.jira_agent import jira_agent
from agents.answer_agent import answer_agent


# ------------------------------------------------------------------
# Agent wrappers (plain functions for LangGraph nodes)
# ------------------------------------------------------------------

def run_slack_branch(state: AgentState) -> AgentState:
    """Invoke slack_agent if activated by orchestrator."""
    if state.get("slack_query"):
        state["slack_result"] = slack_agent.run(
            issues=state["filtered_issues"],
            slack_query=state["slack_query"],
        )
    return state


def run_jira_branch(state: AgentState) -> AgentState:
    """Invoke jira_agent if activated by orchestrator."""
    if state.get("jira_query"):
        state["jira_result"] = jira_agent.run(
            issues=state["filtered_issues"],
            jira_query=state["jira_query"],
        )
    return state


def run_answer_branch(state: AgentState) -> AgentState:
    """Invoke answer_agent for analysis of filtered issues."""
    if state.get("answer_query"):
        state["answer_result"] = answer_agent.analyze_issues(
            issues=state["filtered_issues"],
            answer_query=state["answer_query"],
            output_format=state["enriched_task"]["output_format"],
        )
    return state


def run_query_answer(state: AgentState) -> AgentState:
    """Invoke answer_agent for direct Q&A (no file processing path)."""
    state["answer_result"] = answer_agent.answer_query(
        query=state["instruction"],
        output_format=state["enriched_task"]["output_format"],
    )
    return state


# ------------------------------------------------------------------
# Conditional edge functions
# ------------------------------------------------------------------

def route_by_intent(state: AgentState) -> str:
    """
    [Route 1] After enrichment: does this request need file processing?
    """
    if not state["enriched_task"]["requires_file_processing"]:
        return "query_only"
    return "file_processing"


def route_after_file_parser(state: AgentState) -> str:
    """
    [Route 2] After file parsing: is there a filter_criteria to classify against?
    """
    if state["enriched_task"].get("filter_criteria") is None:
        return "skip_classification"
    return "run_classification"


def route_after_filter(state: AgentState) -> str:
    """
    [Route 3] After filter: are there any matching issues to process?
    """
    if not state.get("filtered_issues"):
        return "early_exit"
    return "continue"


# ------------------------------------------------------------------
# Graph builder
# ------------------------------------------------------------------

def build_graph() -> StateGraph:
    """
    Build and compile the QAIA LangGraph workflow.
    Returns a compiled graph ready for invocation.
    """
    graph = StateGraph(AgentState)

    # Register all nodes
    graph.add_node("enrichment",       enrichment_node)
    graph.add_node("rag",              rag_node)
    graph.add_node("file_parser",      file_parser_node)
    graph.add_node("classification",   classification_node)
    graph.add_node("filter",           filter_node)
    graph.add_node("orchestrator",     orchestrator_node)
    graph.add_node("slack_branch",     run_slack_branch)
    graph.add_node("jira_branch",      run_jira_branch)
    graph.add_node("answer_branch",    run_answer_branch)
    graph.add_node("query_answer",     run_query_answer)
    graph.add_node("aggregator",       aggregator_node)
    graph.add_node("response_builder", response_builder_node)

    # Entry point
    graph.set_entry_point("enrichment")

    # [Route 1] Intent routing: query-only vs file processing
    graph.add_conditional_edges(
        "enrichment",
        route_by_intent,
        {
            "query_only":      "query_answer",
            "file_processing": "rag",
        },
    )

    # [Route 2] After file parser: classify or skip
    graph.add_edge("rag",         "file_parser")
    graph.add_conditional_edges(
        "file_parser",
        route_after_file_parser,
        {
            "run_classification":  "classification",
            "skip_classification": "filter",
        },
    )

    graph.add_edge("classification", "filter")

    # [Route 3] After filter: continue or early exit
    graph.add_conditional_edges(
        "filter",
        route_after_filter,
        {
            "continue":   "orchestrator",
            "early_exit": "response_builder",
        },
    )

    # Orchestrator fans out to all active parallel branches
    graph.add_edge("orchestrator", "slack_branch")
    graph.add_edge("orchestrator", "jira_branch")
    graph.add_edge("orchestrator", "answer_branch")

    # All branches converge at aggregator
    graph.add_edge("slack_branch",  "aggregator")
    graph.add_edge("jira_branch",   "aggregator")
    graph.add_edge("answer_branch", "aggregator")
    graph.add_edge("query_answer",  "aggregator")

    # Final steps
    graph.add_edge("aggregator",       "response_builder")
    graph.add_edge("response_builder", END)

    return graph.compile()
