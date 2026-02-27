"""
Enrichment Node [1/8]

Purpose:
  Transform ANY user instruction into a structured task contract.
  Determines intent, filter criteria, required agents, and output format.

Input:  state["instruction"]   any natural language QA query
Output: state["enriched_task"] structured contract driving all downstream routing

Teaching point:
  The enrichment node is the brain of the system.
  It answers: "What does the user want, and how should the pipeline execute?"

  Example inputs:
    "Find accuracy bugs and post to Slack and create tickets"
    → intent=filter_and_report, requires_file=true, filter_criteria=accuracy,
      requires_slack=true, requires_ticket=true

    "What are common performance issues in ML systems?"
    → intent=query, requires_file=false, requires_analysis=true

    "Create JIRA tickets for all P1 security issues in this file"
    → intent=update, requires_file=true, filter_criteria=security,
      requires_ticket=true
"""

import json
from schemas.state import AgentState
import config


ENRICHMENT_PROMPT = """You are a task contract extractor for a QA intelligence system.

Given a user instruction, extract a structured task contract with these exact fields:

intent: one of:
  - "query"              — user is asking a question, no file processing needed
  - "filter_and_report"  — filter issues from file and report (Slack/JIRA/answer)
  - "analyze"            — analyze issues from file without strict filtering
  - "update"             — create/update JIRA tickets from file

requires_file_processing: true if a file is needed to fulfill the request, false otherwise
  - false for pure questions ("what are...", "how do...", "explain...")
  - true when user says "in this file", "from the file", "uploaded issues", etc.

filter_criteria: object (or null if no filtering needed):
  type: one of "accuracy", "performance", "security", "critical", "custom"
    - "accuracy"    → wrong outputs, calculations, model predictions, data
    - "performance" → slow, latency, timeout, throughput issues
    - "security"    → auth, injection, data exposure, vulnerability
    - "critical"    → P1 or severity=critical issues regardless of type
    - "custom"      → any other specific criteria
  description: 1-2 sentence natural language description of what to look for
  confidence_threshold: float (default 0.6; use 0.8 for "strict/only clear"; 0.4 for "all/any")

requires_slack_post: true if user wants a Slack summary posted
  - keywords: "post", "send", "notify", "slack", "share"

requires_ticket_creation: true if user wants JIRA tickets created
  - keywords: "ticket", "create", "jira", "log", "file", "track"

requires_analysis: true if user wants an inline answer/analysis/summary
  - always true when intent is "query"
  - true when user asks for "summary", "analysis", "breakdown", "explain"
  - false when user only wants Slack/JIRA and no inline answer

output_format: one of "executive" (short, high-level), "detailed" (full breakdown), "bullet" (list)
  - executive: when user says "summary", "brief", "quick", or is engineering manager
  - detailed: when user says "detailed", "full", "breakdown", "explain"
  - bullet: when user asks for a list

User instruction: {instruction}

Return ONLY valid JSON with these exact keys. No explanation. No markdown.
"""


def enrichment_node(state: AgentState) -> AgentState:
    """
    [Node 1] Extract structured task contract from any user instruction.
    Retries once on invalid JSON output.
    """
    # TODO: implement enrichment node
    # Steps:
    #   1. Initialize ChatOpenAI(model=config.LLM_MODEL, temperature=0)
    #   2. Format ENRICHMENT_PROMPT with state["instruction"]
    #   3. Call llm.invoke(prompt) → response
    #   4. json.loads(response.content) → state["enriched_task"]
    #   5. On JSONDecodeError: retry once
    #   6. On second failure: append to state["errors"], raise ValueError
    #   7. Return state
    raise NotImplementedError
