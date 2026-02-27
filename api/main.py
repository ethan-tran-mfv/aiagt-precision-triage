"""
FastAPI Application — Entry point for the QA Intelligence Agent (QAIA).

Endpoint:
  POST /qa-intake
    - Accepts optional QA file upload + required user instruction
    - Initializes AgentState and triggers LangGraph workflow
    - Returns structured response based on intent

Teaching point:
  The API is intentionally thin:
    1. Accept and validate request
    2. Initialize AgentState
    3. Invoke graph → return result
  All intelligence lives in the graph nodes and agents.
"""

import uuid
import os
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional

from graph.workflow import build_graph
from schemas.state import AgentState

app = FastAPI(
    title="QA Intelligence Agent (QAIA)",
    description="Intent-driven AI agent for QA issue analysis, filtering, and reporting",
    version="0.2.0",
)

graph = build_graph()

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".md", ".txt"}


@app.post("/qa-intake")
async def qa_intake(
    instruction: str = Form(..., description="Natural language query or instruction"),
    file: Optional[UploadFile] = None,
):
    """
    Accept any QA instruction with optional file upload.
    The system determines what to do from the instruction alone.

    Examples:
      - instruction="Find accuracy issues and create JIRA tickets", file=issues.csv
      - instruction="What are common performance bugs in ML systems?" (no file)
      - instruction="Summarize all P1 issues", file=issues.csv
    """
    # Validate file type if provided
    raw_content = None
    file_name = None
    if file is not None:
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{file_ext}'. Allowed: {ALLOWED_EXTENSIONS}",
            )
        raw_bytes = await file.read()
        raw_content = raw_bytes.decode("utf-8", errors="replace")
        file_name = file.filename

    # Initialize AgentState
    initial_state: AgentState = {
        "request_id":       str(uuid.uuid4()),
        "trace_id":         str(uuid.uuid4()),
        "instruction":      instruction,
        "raw_file_content": raw_content,
        "file_name":        file_name,
        "enriched_task":    None,
        "rag_context":      None,
        "parsed_issues":    [],
        "classified_issues": [],
        "filtered_issues":  [],
        "slack_query":      None,
        "jira_query":       None,
        "answer_query":     None,
        "slack_result":     None,
        "jira_result":      None,
        "answer_result":    None,
        "errors":           [],
        "metrics":          {},
    }

    # TODO: wrap with LangSmith tracing context (os.environ["LANGCHAIN_TRACING_V2"] = "true")
    final_state = graph.invoke(initial_state)

    return JSONResponse(content=final_state["metrics"].get("response", {}))


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.2.0"}
