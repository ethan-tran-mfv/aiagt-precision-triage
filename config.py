import os
from dotenv import load_dotenv

load_dotenv()

# LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Qdrant
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION_ACCURACY_TAXONOMY = "accuracy_taxonomy"
COLLECTION_JIRA_TICKETS = "jira_tickets"
EMBEDDING_DIMENSION = 1536  # text-embedding-3-small

# RAG
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "4"))
RAG_SCORE_THRESHOLD = float(os.getenv("RAG_SCORE_THRESHOLD", "0.72"))

# Classification
DEFAULT_CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))
CLASSIFICATION_BATCH_SIZE = int(os.getenv("CLASSIFICATION_BATCH_SIZE", "5"))

# Slack
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

# JIRA
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "AIA")
JIRA_DUPLICATE_THRESHOLD = float(os.getenv("JIRA_DUPLICATE_THRESHOLD", "0.90"))

# Observability
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "aia-dev")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")

# Retry
MAX_LLM_RETRIES = 1
MAX_TOOL_RETRIES = 2
