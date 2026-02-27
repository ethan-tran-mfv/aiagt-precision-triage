"""
Answer Agent — NEW

Purpose:
  Handle two distinct scenarios:

  Scenario A — Direct Q&A (no file processing):
    User asks a question. No file uploaded.
    Agent retrieves RAG context from Qdrant and generates a grounded answer.
    Example: "What are common accuracy issues in ML recommendation systems?"

  Scenario B — Issue analysis (file was processed):
    User wants an inline analysis/summary of the filtered issues.
    Agent uses the filtered issues as context + RAG knowledge.
    Example: "Summarize all critical bugs from this file and give me patterns"

Called from:
  - graph/workflow.py directly (Scenario A — query-only path)
  - nodes/orchestrator_node.py (Scenario B — when requires_analysis == True)

Teaching point:
  The answer_agent demonstrates that an agent can serve multiple purposes
  depending on what context it receives. The same agent handles Q&A and
  issue analysis — the difference is in the input, not the agent logic.

  This is different from Slack/JIRA agents which always need filtered issues.
  The answer_agent can operate with OR without file context.
"""

from langchain_openai import ChatOpenAI
from schemas.state import AnswerResult
from agents.rag_agent import rag_agent
import config


ANSWER_PROMPT_QUERY = """You are a QA engineering expert assistant.

Answer the following question using the provided reference knowledge.
Be accurate, practical, and grounded in the retrieved context.

{output_format_instruction}

Reference knowledge:
{rag_context}

Question: {query}
"""

ANSWER_PROMPT_ANALYSIS = """You are a QA analysis expert.

{answer_query}

Filtered QA issues ({issue_count} issues):
{issues_json}

Reference knowledge:
{rag_context}

Provide your analysis in the requested format.
Include: key patterns, severity distribution, and top recommendations.
"""

OUTPUT_FORMAT_INSTRUCTIONS = {
    "executive": "Keep your answer under 200 words. Focus on the most important points.",
    "detailed":  "Provide a thorough, detailed answer with examples and explanations.",
    "bullet":    "Structure your answer as a bullet-point list.",
}


class AnswerAgent:
    def __init__(self, llm=None):
        self.llm = llm or ChatOpenAI(
            model=config.LLM_MODEL,
            openai_api_key=config.OPENAI_API_KEY,
            temperature=0.2,
        )

    def answer_query(self, query: str, output_format: str = "detailed") -> AnswerResult:
        """
        Scenario A: Answer a direct question using RAG context.
        No file or issues context needed.
        """
        # TODO: implement direct Q&A
        # Steps:
        #   1. Retrieve RAG context:
        #        rag_result = rag_agent.retrieve(
        #            query=query,
        #            collection=config.COLLECTION_QA_TAXONOMY,
        #            k=config.RAG_TOP_K,
        #        )
        #   2. Build rag_context string from rag_result["results"]
        #   3. format_instruction = OUTPUT_FORMAT_INSTRUCTIONS.get(output_format, "")
        #   4. Format ANSWER_PROMPT_QUERY with rag_context, query, format_instruction
        #   5. response = self.llm.invoke(prompt)
        #   6. Return AnswerResult(
        #          answer=response.content,
        #          sources=[r.get("source","") for r in rag_result["results"]],
        #          confidence=rag_result["confidence"],
        #      )
        raise NotImplementedError

    def analyze_issues(
        self,
        issues: list[dict],
        answer_query: str,
        output_format: str = "detailed",
    ) -> AnswerResult:
        """
        Scenario B: Analyze filtered issues and return structured summary.
        """
        # TODO: implement issue analysis
        # Steps:
        #   1. Retrieve RAG context for additional grounding:
        #        rag_result = rag_agent.retrieve(
        #            query=answer_query,
        #            collection=config.COLLECTION_QA_TAXONOMY,
        #            k=2,
        #        )
        #   2. Build rag_context string
        #   3. issues_json = json.dumps([{id, title, description} for i in issues], indent=2)
        #   4. Format ANSWER_PROMPT_ANALYSIS with answer_query, issue_count, issues_json, rag_context
        #   5. response = self.llm.invoke(prompt)
        #   6. Return AnswerResult(
        #          answer=response.content,
        #          sources=[],
        #          confidence=1.0,
        #      )
        raise NotImplementedError


# Module-level singleton
answer_agent = AnswerAgent()
