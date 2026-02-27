"""
Qdrant Setup — Initialize collections at system startup.

Run once before starting the API server:
  python rag/setup.py

Creates two collections:
  1. qa_taxonomy    — general QA knowledge (accuracy, performance, security, etc.)
  2. jira_tickets   — created tickets, starts empty, grows as tickets are created

Teaching point:
  The qa_taxonomy collection covers ALL issue types now — not just accuracy.
  The RAG node queries it dynamically based on filter_criteria.type.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import config


def create_collections(client: QdrantClient) -> None:
    """Create all Qdrant collections if they don't already exist."""

    for collection_name in [
        config.COLLECTION_QA_TAXONOMY,
        config.COLLECTION_JIRA_TICKETS,
    ]:
        existing = [c.name for c in client.get_collections().collections]

        if collection_name not in existing:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=config.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE,
                ),
            )
            print(f"Created collection: {collection_name}")
        else:
            print(f"Collection already exists: {collection_name}")


if __name__ == "__main__":
    client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
    create_collections(client)
    print("Qdrant setup complete.")
