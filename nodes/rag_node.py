"""
RAG Node [2/8] — Conditional

Purpose:
  Retrieve relevant QA knowledge from Qdrant based on the filter_criteria.
  Grounds downstream classification in verified knowledge — not LLM assumptions.

Activation condition:
  Only runs when enriched_task["requires_file_processing"] == True
  AND enriched_task["filter_criteria"] is not None.
  (If filter_criteria is null, there is nothing to ground classification on)

Input:  state["enriched_task"]["filter_criteria"]
Output: state["rag_context"]  (RAGResult from rag_agent)

Teaching point:
  The query sent to rag_agent is DYNAMIC — built from filter_criteria.type
  and filter_criteria.description. This is NOT hardcoded to "accuracy".

  filter_criteria.type = "accuracy"    → query about accuracy bugs
  filter_criteria.type = "performance" → query about performance bugs
  filter_criteria.type = "security"    → query about security vulnerabilities
  filter_criteria.type = "custom"      → query using filter_criteria.description directly
"""

from schemas.state import AgentState
from agents.rag_agent import rag_agent
import config


QUERY_TEMPLATES = {
    "accuracy":    "Definition, classification rules, and examples of accuracy-related QA issues, including incorrect outputs, wrong calculations, and misclassified data.",
    "performance": "Definition, classification rules, and examples of performance-related QA issues, including latency bugs, timeout errors, and throughput degradation.",
    "security":    "Definition, classification rules, and examples of security-related QA issues, including authentication failures, injection vulnerabilities, and data exposure.",
    "critical":    "Definition of critical severity QA issues. Issues labelled P1, severity=critical, or causing system outage or data loss.",
}


def rag_node(state: AgentState) -> AgentState:
    """
    [Node 2] Retrieve QA taxonomy from Qdrant, grounded to filter_criteria type.
    """
    # TODO: implement RAG node
    # Steps:
    #   1. criteria = state["enriched_task"]["filter_criteria"]
    #   2. Build query:
    #        if criteria["type"] in QUERY_TEMPLATES → use template
    #        else (type="custom") → use criteria["description"] directly
    #   3. Call rag_agent.retrieve(
    #          query=query,
    #          collection=config.COLLECTION_QA_TAXONOMY,
    #          k=config.RAG_TOP_K,
    #      )
    #   4. If result["results"] is empty:
    #          log warning — proceed with LLM-only classification (degraded mode)
    #          state["rag_context"] = None (classification node handles this)
    #   5. Else: state["rag_context"] = result
    #   6. Return state
    raise NotImplementedError
