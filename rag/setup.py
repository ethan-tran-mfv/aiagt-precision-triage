"""
Qdrant Setup — Initialize collections at system startup.

Run once before starting the API server:
  python rag/setup.py

Creates two collections:
  1. accuracy_taxonomy  — seeded from rag/knowledge/ documents
  2. jira_tickets       — starts empty, grows as tickets are created

Teaching point:
  Separating collections by purpose makes retrieval intent explicit.
  The RAG agent queries the right collection for each use case:
    - Classification grounding  → accuracy_taxonomy
    - Duplicate detection       → jira_tickets
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

import config


def create_collections(client: QdrantClient) -> None:
    """Create both Qdrant collections if they don't already exist."""

    for collection_name in [
        config.COLLECTION_ACCURACY_TAXONOMY,
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
