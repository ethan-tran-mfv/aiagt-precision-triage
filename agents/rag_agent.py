"""
RAG Agent — Retrieval brain for the AIA system.

Responsibilities:
  1. Query rewriting  — expand the query for better semantic recall
  2. Vector search    — query Qdrant with the rewritten query
  3. Re-ranking       — score results by relevance, keep top-k
  4. Context packaging — return a structured result contract

Called by:
  - nodes/rag_node.py       (collection: accuracy_taxonomy)
  - agents/jira_agent.py    (collection: jira_tickets, duplicate detection)
"""

import json
from typing import Optional

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Filter

import config
from schemas.state import RAGResult


QUERY_REWRITE_PROMPT = """You are a semantic search optimizer.
Rewrite the following query to maximize recall in a vector similarity search.
Expand acronyms, add synonyms, and include related concepts.
Return ONLY the rewritten query as a single sentence. No explanation.

Original query: {query}
"""


class RAGAgent:
    def __init__(
        self,
        qdrant_client: Optional[QdrantClient] = None,
        embeddings: Optional[OpenAIEmbeddings] = None,
        llm: Optional[ChatOpenAI] = None,
    ):
        self.client = qdrant_client or QdrantClient(
            host=config.QDRANT_HOST, port=config.QDRANT_PORT
        )
        self.embeddings = embeddings or OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY,
        )
        self.llm = llm or ChatOpenAI(
            model=config.LLM_MODEL,
            openai_api_key=config.OPENAI_API_KEY,
            temperature=0,
        )

    def retrieve(
        self,
        query: str,
        collection: str,
        k: int = config.RAG_TOP_K,
        score_threshold: float = config.RAG_SCORE_THRESHOLD,
        filters: Optional[Filter] = None,
    ) -> RAGResult:
        """
        Main retrieval interface. All callers use this method.

        Args:
            query:            Natural language query
            collection:       Qdrant collection name
            k:                Number of results to return
            score_threshold:  Minimum similarity score (0.0 – 1.0)
            filters:          Optional Qdrant payload filters

        Returns:
            RAGResult with rewritten query, ranked results, and confidence
        """
        # Step 1: Rewrite the query for better semantic coverage
        rewritten_query = self._rewrite_query(query)

        # Step 2: Embed and search Qdrant
        raw_results = self._search(
            query=rewritten_query,
            collection=collection,
            k=k + 1,  # fetch one extra for re-ranking headroom
            score_threshold=score_threshold,
            filters=filters,
        )

        # Step 3: Re-rank by relevance to the ORIGINAL query, keep top k
        ranked_results = self._rerank(
            results=raw_results,
            original_query=query,
            k=k,
        )

        # Step 4: Package and return structured result
        top_score = ranked_results[0]["score"] if ranked_results else 0.0

        return RAGResult(
            query=query,
            rewritten_query=rewritten_query,
            results=[r["payload"] for r in ranked_results],
            confidence=round(top_score, 4),
            source_collection=collection,
        )

    # ------------------------------------------------------------------
    # Private methods
    # ------------------------------------------------------------------

    def _rewrite_query(self, query: str) -> str:
        """
        Use LLM to expand the query for better semantic recall.

        Example:
          Input:  "accuracy-related QA issues"
          Output: "software quality issues involving incorrect outputs,
                   wrong calculations, misclassified data, or inaccurate
                   numerical results in production systems"
        """
        # TODO: implement LLM query rewriting
        # Hint: use self.llm.invoke() with QUERY_REWRITE_PROMPT
        # Return the rewritten query string
        # On failure, fall back to original query
        raise NotImplementedError

    def _search(
        self,
        query: str,
        collection: str,
        k: int,
        score_threshold: float,
        filters: Optional[Filter],
    ) -> list[dict]:
        """
        Embed the query and perform vector similarity search in Qdrant.

        Returns list of dicts with keys: id, score, payload
        """
        # TODO: implement Qdrant search
        # Hint:
        #   1. vector = self.embeddings.embed_query(query)
        #   2. results = self.client.search(
        #          collection_name=collection,
        #          query_vector=vector,
        #          limit=k,
        #          score_threshold=score_threshold,
        #          query_filter=filters,
        #      )
        #   3. return [{"id": r.id, "score": r.score, "payload": r.payload} for r in results]
        raise NotImplementedError

    def _rerank(self, results: list[dict], original_query: str, k: int) -> list[dict]:
        """
        Re-rank results by relevance to the original (non-rewritten) query.
        Keeps top k results.

        Simple strategy: re-score using dot product against original query embedding.
        Advanced strategy: use a cross-encoder or LLM-based reranker.
        """
        # TODO: implement re-ranking
        # Simple approach:
        #   1. Embed the original_query
        #   2. For each result, compute cosine similarity between
        #      original_query embedding and result payload text embedding
        #   3. Sort by new score, return top k
        # Fallback: return results[:k] sorted by existing score
        raise NotImplementedError


# Module-level singleton — shared across all callers
rag_agent = RAGAgent()
