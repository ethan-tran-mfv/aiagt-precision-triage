"""
JIRA Agent

Purpose:
  Create JIRA tickets for each accuracy issue, with duplicate detection via RAG.
  Called by the orchestrator node as one of two parallel branches.

Input:
  issues:      list of accuracy-related ClassifiedIssue dicts
  jira_query:  specialized instruction from orchestrator_node

Output:
  JiraResult with lists of created tickets and detected duplicates

Flow (per issue):
  1. Check for duplicate via rag_agent (collection: jira_tickets)
  2. If similarity >= JIRA_DUPLICATE_THRESHOLD → skip, record as duplicate
  3. Else → generate ticket content (LLM) → create via JIRA API
  4. Store new ticket embedding in Qdrant (jira_tickets collection)

Parallelization:
  All ticket creation calls use asyncio.gather() — max concurrency: 5
  (prevents JIRA API rate limiting)

Teaching point:
  The JIRA agent uses rag_agent internally for duplicate detection.
  This is an agent calling another agent — a key agentic architecture pattern.
  The jira_tickets Qdrant collection grows as tickets are created,
  making duplicate detection smarter over time.
"""

import asyncio
from jira import JIRA

from schemas.state import JiraResult
from agents.rag_agent import rag_agent
import config


TICKET_PROMPT = """You are a JIRA ticket writer for a QA engineering team.

{jira_query}

Issue to ticket:
{issue_json}

Generate a structured JIRA ticket with these fields:
- summary: one-line ticket title (max 100 chars)
- description: full issue description with reproduction steps
- expected: expected behavior
- actual: actual (incorrect) behavior
- priority: P1 (critical accuracy loss) | P2 (significant) | P3 (minor)

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
        """
        Process all issues: duplicate check → ticket creation (parallel).
        Returns JiraResult with created and duplicates lists.
        """
        return asyncio.run(self._run_async(issues, jira_query))

    async def _run_async(self, issues: list[dict], jira_query: str) -> JiraResult:
        """
        Run all ticket operations concurrently (max MAX_CONCURRENT_TICKETS at once).
        """
        # TODO: implement async ticket processing
        # Steps:
        #   1. semaphore = asyncio.Semaphore(MAX_CONCURRENT_TICKETS)
        #   2. tasks = [self._process_issue(issue, jira_query, semaphore) for issue in issues]
        #   3. results = await asyncio.gather(*tasks, return_exceptions=True)
        #   4. Separate results into created[] and duplicates[]
        #   5. Return JiraResult(created=created, duplicates=duplicates, success=True, error=None)
        raise NotImplementedError

    async def _process_issue(
        self, issue: dict, jira_query: str, semaphore: asyncio.Semaphore
    ) -> dict:
        """
        For a single issue: check duplicate → create ticket or skip.
        """
        # TODO: implement per-issue processing
        # Steps:
        #   1. async with semaphore:
        #   2. Check duplicate:
        #        rag_result = rag_agent.retrieve(
        #            query=issue["title"] + " " + issue["description"],
        #            collection=config.COLLECTION_JIRA_TICKETS,
        #            k=1,
        #            score_threshold=config.JIRA_DUPLICATE_THRESHOLD,
        #        )
        #   3. If rag_result["confidence"] >= config.JIRA_DUPLICATE_THRESHOLD:
        #        return {"type": "duplicate", "issue_id": issue["id"],
        #                "existing_ticket": rag_result["results"][0]}
        #   4. Else: generate ticket content → create in JIRA API
        #        a. Format TICKET_PROMPT with jira_query + issue_json
        #        b. Call llm → parse JSON ticket fields
        #        c. self.client.create_issue(fields={...})
        #        d. Store ticket in rag_agent jira_tickets collection
        #        e. Return {"type": "created", "issue_id": ..., "url": ...}
        raise NotImplementedError


# Module-level singleton
jira_agent = JiraAgent()
