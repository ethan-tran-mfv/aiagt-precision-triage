"""
RAG Node [2/8]

Purpose:
  Retrieve the accuracy definition and taxonomy from Qdrant.
  Grounds all downstream classification in verified knowledge — not LLM assumptions.

Input:  state["enriched_task"]       (uses task_type as query seed)
Output: state["accuracy_definition"] (RAGResult from rag_agent)

Teaching point:
  This node is intentionally thin — it delegates ALL retrieval intelligence
  to rag_agent.py. The node only knows WHAT to retrieve; the agent knows HOW.

  Node  = decides what to retrieve (which collection, what query)
  Agent = decides how to retrieve  (query rewriting, search, reranking)
"""

from schemas.state import AgentState
from agents.rag_agent import rag_agent
import config


ACCURACY_QUERY = (
    "Definition and classification rules for accuracy-related QA issues, "
    "including examples of accuracy bugs and non-accuracy bugs."
)


def rag_node(state: AgentState) -> AgentState:
    """
    [Node 2] Retrieve accuracy taxonomy from Qdrant via rag_agent.
    Aborts workflow if RAG returns empty results (no grounding available).
    """
    # TODO: implement RAG node
    # Steps:
    #   1. Call rag_agent.retrieve(
    #          query=ACCURACY_QUERY,
    #          collection=config.COLLECTION_ACCURACY_TAXONOMY,
    #          k=config.RAG_TOP_K,
    #      )
    #   2. If result["results"] is empty:
    #          append error to state["errors"]
    #          raise ValueError("RAG returned empty — cannot classify without taxonomy")
    #   3. Set state["accuracy_definition"] = result
    #   4. Return state
    raise NotImplementedError
