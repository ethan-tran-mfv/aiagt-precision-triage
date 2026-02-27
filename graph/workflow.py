"""
LangGraph Workflow — Defines the full AIA execution graph.

This file is the single source of truth for the system's execution order.
Reading this file tells you everything about how the system runs.

Node execution order:
  [1] enrichment_node      — intent → task contract
  [2] rag_node             — retrieve accuracy taxonomy
  [3] file_parser_node     — parse uploaded file
  [4] classification_node  — classify issues (LLM + RAG)
  [5] filter_node          — apply confidence threshold
  [6] orchestrator_node    — generate sub-agent queries
  [7a] slack_agent         — (parallel) post summary to Slack
  [7b] jira_agent          — (parallel) create JIRA tickets
  [8] aggregator_node      — merge parallel results
  [9] response_builder_node — build final API response

Graph features demonstrated:
  - Sequential node chaining
  - Conditional edge (early exit if no accuracy issues found)
  - Parallel branch execution (Slack + JIRA)
  - Branch convergence at aggregator

Teaching point:
  The entire system architecture is visible in build_graph().
  Each add_node() call = one lecture topic.
  Each add_edge() call = one data dependency.
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


def run_slack_branch(state: AgentState) -> AgentState:
    """Wrapper: invoke slack_agent and store result in state."""
    if state.get("slack_query"):
        state["slack_result"] = slack_agent.run(
            issues=state["accuracy_issues"],
            slack_query=state["slack_query"],
        )
    return state


def run_jira_branch(state: AgentState) -> AgentState:
    """Wrapper: invoke jira_agent and store result in state."""
    if state.get("jira_query"):
        state["jira_result"] = jira_agent.run(
            issues=state["accuracy_issues"],
            jira_query=state["jira_query"],
        )
    return state


def should_continue(state: AgentState) -> str:
    """
    Conditional edge after filter_node.
    If no accuracy issues found → go directly to response_builder (early exit).
    Otherwise → proceed to orchestrator.
    """
    if not state.get("accuracy_issues"):
        return "early_exit"
    return "continue"


def build_graph() -> StateGraph:
    """
    Build and compile the AIA LangGraph workflow.
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
    graph.add_node("aggregator",       aggregator_node)
    graph.add_node("response_builder", response_builder_node)

    # Entry point
    graph.set_entry_point("enrichment")

    # Sequential edges
    graph.add_edge("enrichment",     "rag")
    graph.add_edge("rag",            "file_parser")
    graph.add_edge("file_parser",    "classification")
    graph.add_edge("classification", "filter")

    # Conditional edge: early exit if no accuracy issues found
    graph.add_conditional_edges(
        "filter",
        should_continue,
        {
            "continue":   "orchestrator",
            "early_exit": "response_builder",
        },
    )

    # Orchestrator fans out to parallel branches
    graph.add_edge("orchestrator", "slack_branch")
    graph.add_edge("orchestrator", "jira_branch")

    # Parallel branches converge at aggregator
    graph.add_edge("slack_branch", "aggregator")
    graph.add_edge("jira_branch",  "aggregator")

    # Final step
    graph.add_edge("aggregator",       "response_builder")
    graph.add_edge("response_builder", END)

    return graph.compile()
