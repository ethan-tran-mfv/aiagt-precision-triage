"""
Integration tests for RAG agent.
Requires: Qdrant running + knowledge base ingested.

  docker-compose up -d
  python rag/setup.py && python rag/ingest.py
  pytest tests/integration/test_rag_retrieval.py -v
"""

import pytest
from agents.rag_agent import RAGAgent
import config


@pytest.fixture(scope="module")
def agent():
    return RAGAgent()


def test_retrieve_returns_results(agent):
    result = agent.retrieve(
        query="What is an accuracy-related bug?",
        collection=config.COLLECTION_ACCURACY_TAXONOMY,
        k=3,
    )
    assert len(result["results"]) > 0
    assert result["confidence"] > 0.0
    assert result["source_collection"] == config.COLLECTION_ACCURACY_TAXONOMY


def test_retrieve_rewrites_query(agent):
    result = agent.retrieve(
        query="accuracy issues",
        collection=config.COLLECTION_ACCURACY_TAXONOMY,
    )
    assert len(result["rewritten_query"]) > len("accuracy issues")


def test_high_threshold_filters_unrelated_query(agent):
    result = agent.retrieve(
        query="unrelated topic about food recipes",
        collection=config.COLLECTION_ACCURACY_TAXONOMY,
        score_threshold=0.90,
    )
    assert result["confidence"] < 0.90 or len(result["results"]) == 0


def test_result_has_correct_structure(agent):
    result = agent.retrieve(
        query="numerical calculation error",
        collection=config.COLLECTION_ACCURACY_TAXONOMY,
    )
    for key in ("query", "rewritten_query", "results", "confidence", "source_collection"):
        assert key in result
