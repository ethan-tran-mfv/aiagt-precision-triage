"""
Slack Agent

Purpose:
  Generate a formatted summary of QA issues and post it to Slack.
  Called by the orchestrator when requires_slack_post == True.

Input:
  issues:       list of filtered issue dicts
  slack_query:  specialized instruction from orchestrator_node
                (includes criteria description, output format, focus area)

Output:
  SlackResult with summary_markdown, slack_url, success flag

Flow:
  1. Generate summary using LLM (guided by slack_query)
  2. Format as Slack markdown blocks
  3. Post to Slack API (with retry)
  4. Return SlackResult

Teaching point:
  The slack_query is purpose-built by the orchestrator for this specific request.
  It includes the filter criteria context, output format, and focus area.
  The agent doesn't need to know what kind of issues these are — the query tells it.
"""

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from schemas.state import SlackResult
import config


SUMMARY_PROMPT = """You are an engineering communication specialist.

{slack_query}

Issues to summarize:
{issues_json}

Format your response as Slack-compatible markdown.
"""


class SlackAgent:
    def __init__(self, slack_client=None):
        self.client = slack_client or WebClient(token=config.SLACK_BOT_TOKEN)

    def run(self, issues: list[dict], slack_query: str) -> SlackResult:
        """
        Generate summary and post to Slack. Returns SlackResult.
        """
        # TODO: implement Slack agent
        # Steps:
        #   1. Initialize ChatOpenAI(model=config.LLM_MODEL, temperature=0.2)
        #   2. issues_json = json.dumps([{id, title, description} for i in issues])
        #   3. Format SUMMARY_PROMPT with slack_query + issues_json
        #   4. response = llm.invoke(prompt) → summary_markdown string
        #   5. Post with retry:
        #        for attempt in range(config.MAX_TOOL_RETRIES + 1):
        #            try:
        #                resp = self.client.chat_postMessage(
        #                    channel=config.SLACK_CHANNEL_ID,
        #                    text=summary_markdown,
        #                )
        #                return SlackResult(
        #                    summary_markdown=summary_markdown,
        #                    slack_url=resp.get("message", {}).get("permalink"),
        #                    success=True, error=None,
        #                )
        #            except SlackApiError as e:
        #                if attempt == config.MAX_TOOL_RETRIES:
        #                    return SlackResult(
        #                        summary_markdown=summary_markdown,
        #                        slack_url=None, success=False, error=str(e),
        #                    )
        raise NotImplementedError


# Module-level singleton
slack_agent = SlackAgent()
