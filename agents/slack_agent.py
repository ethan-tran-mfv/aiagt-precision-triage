"""
Slack Agent

Purpose:
  Generate an executive markdown summary of accuracy issues and post it to Slack.
  Called by the orchestrator node as one of two parallel branches.

Input:
  issues:       list of accuracy-related ClassifiedIssue dicts
  slack_query:  specialized instruction from orchestrator_node

Output:
  SlackResult with summary_markdown, slack_url, success flag

Flow:
  1. Generate summary (LLM call using slack_query + issues)
  2. Format as Slack markdown blocks
  3. Post to Slack API
  4. Return SlackResult

Error handling:
  - Retry Slack API call up to config.MAX_TOOL_RETRIES times
  - On final failure: return SlackResult with success=False, error=message
  - Failure does NOT stop the JIRA branch (failure isolation)

Teaching point:
  Sub-agents are NOT LangGraph nodes — they are plain Python classes/functions
  called by the orchestrator. They have their own retry logic and error handling
  independent of the graph.
"""

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from schemas.state import SlackResult
import config


SUMMARY_PROMPT = """You are an engineering communication specialist.

{slack_query}

Accuracy-related issues:
{issues_json}

Format your response as Slack-compatible markdown.
Keep it under 300 words. Focus on production risk and business impact.
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
        #   1. Generate markdown summary:
        #        a. Initialize ChatOpenAI
        #        b. Format SUMMARY_PROMPT with slack_query + issues_json
        #        c. Call llm.invoke(prompt) → summary_markdown string
        #   2. Post to Slack with retry:
        #        for attempt in range(config.MAX_TOOL_RETRIES + 1):
        #            try:
        #                response = self.client.chat_postMessage(
        #                    channel=config.SLACK_CHANNEL_ID,
        #                    text=summary_markdown,
        #                )
        #                return SlackResult(
        #                    summary_markdown=summary_markdown,
        #                    slack_url=response["message"]["permalink"],
        #                    success=True,
        #                    error=None,
        #                )
        #            except SlackApiError as e:
        #                if attempt == config.MAX_TOOL_RETRIES:
        #                    return SlackResult(..., success=False, error=str(e))
        raise NotImplementedError


# Module-level singleton
slack_agent = SlackAgent()
