"""
Classification Node [4/8]

Purpose:
  Classify each parsed issue as accuracy-related or not, using:
    - RAG-retrieved accuracy taxonomy (semantic grounding)
    - LLM reasoning per issue

Input:
  state["parsed_issues"]       list of ParsedIssue
  state["accuracy_definition"] RAGResult from rag_node

Output:
  state["classified_issues"]   list of ClassifiedIssue

Teaching point:
  Issues are classified in BATCHES (default: 5) to reduce LLM calls.
  The RAG context is injected into every batch prompt — this is
  RAG-grounded classification, not pure LLM guessing.
  Experiment: change CLASSIFICATION_BATCH_SIZE and observe latency vs accuracy.
"""

import json
from schemas.state import AgentState
import config


CLASSIFICATION_PROMPT = """You are a QA issue classifier specializing in accuracy-related bugs.

Accuracy Definition (from internal taxonomy):
{accuracy_context}

Classify each of the following QA issues. For each issue determine:
- accuracy_related: true/false
- confidence: float between 0.0 and 1.0
- reason: one sentence explaining your decision

Issues to classify:
{issues_json}

Return a JSON array — one object per issue:
[
  {{
    "issue_id": "...",
    "accuracy_related": true,
    "confidence": 0.85,
    "reason": "..."
  }}
]

Return ONLY the JSON array. No explanation. No markdown.
"""


def classification_node(state: AgentState) -> AgentState:
    """
    [Node 4] Classify all parsed issues in batches using LLM + RAG context.
    """
    # TODO: implement classification node
    # Steps:
    #   1. Extract accuracy context string from state["accuracy_definition"]["results"]
    #      (join all result texts)
    #   2. Split state["parsed_issues"] into batches of config.CLASSIFICATION_BATCH_SIZE
    #   3. For each batch:
    #        a. Format CLASSIFICATION_PROMPT with accuracy_context + issues_json
    #        b. Call llm.invoke(prompt)
    #        c. Parse JSON response → list of ClassifiedIssue dicts
    #        d. On JSONDecodeError: retry once (config.MAX_LLM_RETRIES)
    #   4. Collect all results → state["classified_issues"]
    #   5. Return state
    raise NotImplementedError


def _extract_accuracy_context(rag_result: dict) -> str:
    """Join RAG result chunks into a single context string for the prompt."""
    # TODO: join rag_result["results"] texts into one string
    raise NotImplementedError


def _format_issues_for_prompt(issues: list[dict]) -> str:
    """Format a batch of issues as compact JSON (id, title, description only)."""
    # TODO: return json.dumps of trimmed issue dicts
    raise NotImplementedError
