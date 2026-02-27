"""
Enrichment Node [1/8]

Purpose:
  Transform ambiguous user instruction into a structured task contract.
  Prevents blind orchestration by making intent explicit before processing.

Input:  state["instruction"]   e.g. "Summarize accuracy issues and create tickets"
Output: state["enriched_task"] e.g. {task_type, requires_slack_post, ...}

Teaching point:
  This node answers: "What does the user actually want?"
  Raw user text is never passed downstream — only the structured contract.
"""

import json
from schemas.state import AgentState
import config


ENRICHMENT_PROMPT = """You are a task contract extractor for a QA issue processing system.

Given a user instruction, extract a structured task contract with these exact fields:
- task_type: always "accuracy_filter" for this system
- requires_slack_post: true if user wants a Slack summary posted
- requires_ticket_creation: true if user wants JIRA tickets created
- confidence_threshold: strictness of classification (float, default: 0.6)

Rules:
- "summarize", "post", "notify", "send"      → requires_slack_post = true
- "ticket", "create", "log", "file", "jira"  → requires_ticket_creation = true
- "strict", "only clear", "confident"        → confidence_threshold = 0.8
- "all", "everything", "any"                 → confidence_threshold = 0.4
- If ambiguous → both true, threshold 0.6

User instruction: {instruction}

Return ONLY valid JSON. No explanation. No markdown.
"""


def enrichment_node(state: AgentState) -> AgentState:
    """
    [Node 1] Enrich user instruction into a structured task contract.
    Retries once on invalid JSON output.
    """
    # TODO: implement enrichment node
    # Steps:
    #   1. Initialize ChatOpenAI with config.LLM_MODEL
    #   2. Format ENRICHMENT_PROMPT with state["instruction"]
    #   3. Call llm.invoke(prompt)
    #   4. Parse response as JSON → state["enriched_task"]
    #   5. On JSONDecodeError: retry once
    #   6. On second failure: raise ValueError, append to state["errors"]
    raise NotImplementedError
