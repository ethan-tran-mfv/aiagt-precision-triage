"""
FastAPI Application — Entry point for the AIA system.

Endpoint:
  POST /qa-intake
    - Accepts QA file upload + user instruction
    - Generates request_id and trace_id
    - Triggers LangGraph workflow
    - Returns final structured response

Teaching point:
  The API layer is kept thin on purpose. It does three things only:
    1. Accept and validate the request
    2. Initialize the AgentState
    3. Invoke the graph and return the result
  All business logic lives in the graph nodes and agents.
"""

import uuid
import os
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse

from graph.workflow import build_graph
from schemas.state import AgentState

app = FastAPI(
    title="Accuracy Intelligence Agent (AIA)",
    description="Production-grade AI workflow for QA issue accuracy classification",
    version="0.1.0",
)

graph = build_graph()


@app.post("/qa-intake")
async def qa_intake(
    file: UploadFile,
    instruction: str = Form(default="Summarize accuracy issues and create tickets"),
):
    """
    Accept a QA issue file and an optional instruction.
    Run the full AIA workflow and return the structured result.
    """
    # Validate file type
    allowed_extensions = {".csv", ".xlsx", ".md", ".txt"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file_ext}'. Allowed: {allowed_extensions}",
        )

    # Read file content
    raw_content = await file.read()

    # Initialize AgentState
    initial_state: AgentState = {
        "request_id": str(uuid.uuid4()),
        "trace_id": str(uuid.uuid4()),
        "instruction": instruction,
        "raw_file_content": raw_content.decode("utf-8", errors="replace"),
        "file_name": file.filename,
        "enriched_task": None,
        "accuracy_definition": None,
        "parsed_issues": [],
        "classified_issues": [],
        "accuracy_issues": [],
        "slack_query": None,
        "jira_query": None,
        "slack_result": None,
        "jira_result": None,
        "errors": [],
        "metrics": {},
    }

    # Run the LangGraph workflow
    # TODO: wrap with LangSmith tracing context
    final_state = graph.invoke(initial_state)

    return JSONResponse(content=final_state["metrics"].get("response", {}))


@app.get("/health")
def health():
    return {"status": "ok"}
