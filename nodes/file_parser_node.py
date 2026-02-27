"""
File Parser Node [3/8]

Purpose:
  Parse uploaded QA file into a normalized list of issues.
  No LLM involved — pure deterministic parsing.

Supported formats: CSV, Excel (.xlsx), Markdown, TXT

Input:  state["raw_file_content"], state["file_name"]
Output: state["parsed_issues"]  list of ParsedIssue dicts

Expected columns (case-insensitive): id, title, description, steps, severity

Teaching point:
  This is the only node with zero LLM calls.
  Deterministic parsing keeps the graph predictable and fast.
  Always normalize at the boundary before LLM processing.
"""

from schemas.state import AgentState, ParsedIssue


REQUIRED_FIELDS = {"id", "title", "description"}
OPTIONAL_FIELDS = {"steps", "severity"}


def file_parser_node(state: AgentState) -> AgentState:
    """
    [Node 3] Parse raw file content into normalized ParsedIssue list.
    """
    # TODO: implement file parser node
    # Steps:
    #   1. Detect format from state["file_name"] extension (.csv/.xlsx/.md/.txt)
    #   2. Dispatch to the correct private parser
    #   3. Normalize column names to lowercase
    #   4. Validate REQUIRED_FIELDS are present, raise ValueError if missing
    #   5. Fill missing OPTIONAL_FIELDS with empty string ""
    #   6. Set state["parsed_issues"] = list of ParsedIssue dicts
    #   7. Return state
    raise NotImplementedError


def _parse_csv(content: str) -> list[dict]:
    # TODO: use csv.DictReader to parse CSV content string
    raise NotImplementedError


def _parse_excel(content: bytes) -> list[dict]:
    # TODO: use pd.read_excel(io.BytesIO(content)) to parse Excel bytes
    raise NotImplementedError


def _parse_markdown(content: str) -> list[dict]:
    # TODO: parse markdown table rows into dicts
    raise NotImplementedError


def _parse_txt(content: str) -> list[dict]:
    # TODO: each non-empty line = one issue title, auto-generate id
    raise NotImplementedError


def _normalize(issues: list[dict]) -> list[ParsedIssue]:
    """Lowercase keys, fill missing optional fields, cast to ParsedIssue."""
    # TODO: normalize each issue dict into ParsedIssue TypedDict
    raise NotImplementedError
