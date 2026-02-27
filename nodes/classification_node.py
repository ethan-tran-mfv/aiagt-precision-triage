"""
Classification Node [4/8] — Conditional

Purpose:
  Classify each parsed issue against the DYNAMIC filter_criteria.
  Uses RAG-retrieved taxonomy context (or LLM-only if RAG returned empty).

Activation condition:
  Only runs when enriched_task["filter_criteria"] is not None.
  If filter_criteria is null (e.g., "summarize all issues"), this node is skipped
  and all parsed issues pass through to the filter node unchanged.

Input:
  state["parsed_issues"]       list of ParsedIssue
  state["rag_context"]         RAGResult (may be None — degraded mode)
  state["enriched_task"]["filter_criteria"]  the dynamic criteria to classify against

Output:
  state["classified_issues"]   list of ClassifiedIssue

Teaching point:
  The classification prompt uses filter_criteria.description as the classification
  target — NOT a hardcoded concept. This makes the same node work for:
    - accuracy issues
    - performance issues
    - security vulnerabilities
    - any custom criteria the user specifies

  Experiment: change filter_criteria.type and observe different issues being flagged.
"""

import json
from schemas.state import AgentState
import config


CLASSIFICATION_PROMPT = """You are a QA issue classifier.

Classification target:
Type: {criteria_type}
Description: {criteria_description}

{rag_context_section}

Classify each of the following QA issues. For each issue determine:
- matches_criteria: true if the issue matches the classification target above
- confidence: float between 0.0 and 1.0
- reason: one sentence explaining your decision

Issues to classify:
{issues_json}

Return a JSON array — one object per issue:
[
  {{
    "issue_id": "...",
    "matches_criteria": true,
    "confidence": 0.85,
    "reason": "..."
  }}
]

Return ONLY the JSON array. No explanation. No markdown.
"""

RAG_CONTEXT_SECTION = """Reference knowledge (use this to inform your classification):
{rag_context}
"""

NO_RAG_SECTION = "Note: No reference knowledge available. Use your expert judgment only."


def classification_node(state: AgentState) -> AgentState:
    """
    [Node 4] Classify issues against dynamic filter_criteria in batches.
    """
    # TODO: implement classification node
    # Steps:
    #   1. criteria = state["enriched_task"]["filter_criteria"]
    #   2. Build rag_context_section:
    #        if state["rag_context"] and state["rag_context"]["results"]:
    #            rag_text = "\n".join([r.get("text","") for r in state["rag_context"]["results"]])
    #            rag_context_section = RAG_CONTEXT_SECTION.format(rag_context=rag_text)
    #        else:
    #            rag_context_section = NO_RAG_SECTION
    #   3. Split state["parsed_issues"] into batches of CLASSIFICATION_BATCH_SIZE
    #   4. For each batch:
    #        a. Format CLASSIFICATION_PROMPT with criteria + rag_context_section + issues_json
    #        b. llm.invoke(prompt)
    #        c. json.loads(response.content) → list of ClassifiedIssue
    #        d. On JSONDecodeError: retry once
    #   5. state["classified_issues"] = all results
    #   6. Return state
    raise NotImplementedError


def _format_issues_for_prompt(issues: list[dict]) -> str:
    """Format a batch of issues as compact JSON (id, title, description only)."""
    raise NotImplementedError
