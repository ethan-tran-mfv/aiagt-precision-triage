"""
JIRA Agent

Purpose:
  Create JIRA tickets for each filtered issue, with duplicate detection via RAG.
  Called by the orchestrator when requires_ticket_creation == True.

Input:
  issues:      list of filtered issue dicts
  jira_query:  specialized instruction from orchestrator_node

Output:
  JiraResult with lists of created tickets and detected duplicates

Flow (per issue):
  1. Check for duplicate via rag_agent (collection: jira_tickets)
  2. If similarity >= JIRA_DUPLICATE_THRESHOLD → skip, record as duplicate
  3. Else → generate ticket content (LLM) → create via JIRA API
  4. Store new ticket embedding in Qdrant jira_tickets collection

Parallelization:
  All ticket operations use asyncio.gather() — max concurrency: 5

Teaching point:
  The JIRA agent calls rag_agent internally for duplicate detection.
  This is an agent calling another agent — a key agentic architecture pattern.
  The jira_tickets collection grows as tickets are created, making duplicate
  detection smarter over time (self-improving system).
"""

import asyncio
from jira import JIRA

from schemas.state import JiraResult
from agents.rag_agent import rag_agent
import config


TICKET_PROMPT = """You are a JIRA ticket writer for a QA engineering team.

{jira_query}

Issue to create a ticket for:
{issue_json}

Generate a structured JIRA ticket with these exact fields:
- summary: one-line title (max 100 chars)
- description: full description with context
- steps: reproduction steps
- expected: expected behavior
- actual: actual (incorrect) behavior
- priority: P1 (critical/blocker) | P2 (significant) | P3 (minor)

Return ONLY valid JSON with these exact keys. No markdown.
"""

MAX_CONCURRENT_TICKETS = 5


class JiraAgent:
    def __init__(self, jira_client=None):
        self.client = jira_client or JIRA(
            server=config.JIRA_URL,
            basic_auth=(config.JIRA_EMAIL, config.JIRA_API_TOKEN),
        )

    def run(self, issues: list[dict], jira_query: str) -> JiraResult:
        """Process all issues: duplicate check → ticket creation (parallel)."""
        return asyncio.run(self._run_async(issues, jira_query))

    async def _run_async(self, issues: list[dict], jira_query: str) -> JiraResult:
        """Run all ticket operations concurrently (max MAX_CONCURRENT_TICKETS)."""
        # TODO: implement async ticket processing
        # Steps:
        #   1. semaphore = asyncio.Semaphore(MAX_CONCURRENT_TICKETS)
        #   2. tasks = [self._process_issue(i, jira_query, semaphore) for i in issues]
        #   3. results = await asyncio.gather(*tasks, return_exceptions=True)
        #   4. created = [r for r in results if r.get("type") == "created"]
        #   5. duplicates = [r for r in results if r.get("type") == "duplicate"]
        #   6. Return JiraResult(created=created, duplicates=duplicates, success=True, error=None)
        raise NotImplementedError

    async def _process_issue(
        self, issue: dict, jira_query: str, semaphore: asyncio.Semaphore
    ) -> dict:
        """For a single issue: duplicate check → create or skip."""
        # TODO: implement per-issue processing
        # Steps:
        #   async with semaphore:
        #   1. Check duplicate via rag_agent:
        #        result = rag_agent.retrieve(
        #            query=issue.get("title","") + " " + issue.get("description",""),
        #            collection=config.COLLECTION_JIRA_TICKETS,
        #            k=1,
        #            score_threshold=config.JIRA_DUPLICATE_THRESHOLD,
        #        )
        #   2. If result["confidence"] >= config.JIRA_DUPLICATE_THRESHOLD:
        #        return {"type": "duplicate", "issue_id": issue["id"],
        #                "existing": result["results"][0] if result["results"] else {}}
        #   3. Else:
        #        a. Format TICKET_PROMPT with jira_query + issue_json
        #        b. llm.invoke(prompt) → parse JSON ticket fields
        #        c. jira_issue = self.client.create_issue(fields={
        #               "project": {"key": config.JIRA_PROJECT_KEY},
        #               "summary": ticket["summary"],
        #               "description": ticket["description"],
        #               "issuetype": {"name": "Bug"},
        #               "priority": {"name": ticket["priority"]},
        #           })
        #        d. Return {"type": "created", "issue_id": issue["id"],
        #                   "url": jira_issue.permalink()}
        raise NotImplementedError


# Module-level singleton
jira_agent = JiraAgent()
