"""
RAG Ingestion — Embed and store knowledge documents into Qdrant.

Run after setup.py:
  python rag/ingest.py

Reads all .md files from rag/knowledge/, splits them into chunks,
embeds them with OpenAI, and upserts into the accuracy_taxonomy collection.

Teaching point:
  The quality of what's in rag/knowledge/ directly controls classification quality.
  Lab exercise: add more examples to accuracy_taxonomy.md and observe
  how precision improves in Langfuse metrics.
"""

from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import MarkdownTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

import config


KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def ingest_knowledge_base(client: QdrantClient = None) -> int:
    """
    Load, split, embed, and store all knowledge documents.
    Returns the number of chunks ingested.
    """
    client = client or QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
    embeddings = OpenAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        openai_api_key=config.OPENAI_API_KEY,
    )

    # Load all markdown files from knowledge directory
    loader = DirectoryLoader(
        str(KNOWLEDGE_DIR),
        glob="*.md",
        loader_cls=TextLoader,
    )
    docs = loader.load()

    if not docs:
        raise FileNotFoundError(f"No documents found in {KNOWLEDGE_DIR}")

    # Split into chunks
    splitter = MarkdownTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(docs)

    # Embed and upsert into Qdrant
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=f"http://{config.QDRANT_HOST}:{config.QDRANT_PORT}",
        collection_name=config.COLLECTION_ACCURACY_TAXONOMY,
    )

    print(f"Ingested {len(chunks)} chunks into '{config.COLLECTION_ACCURACY_TAXONOMY}'")
    return len(chunks)


if __name__ == "__main__":
    ingest_knowledge_base()
