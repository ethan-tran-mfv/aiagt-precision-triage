from typing import TypedDict, Optional


class EnrichedTask(TypedDict):
    task_type: str
    requires_slack_post: bool
    requires_ticket_creation: bool
    confidence_threshold: float


class ParsedIssue(TypedDict):
    id: str
    title: str
    description: str
    steps: str
    severity: str


class ClassifiedIssue(TypedDict):
    issue_id: str
    accuracy_related: bool
    confidence: float
    reason: str


class RAGResult(TypedDict):
    query: str
    rewritten_query: str
    results: list[dict]
    confidence: float
    source_collection: str


class SlackResult(TypedDict):
    summary_markdown: str
    slack_url: str
    success: bool
    error: Optional[str]


class JiraResult(TypedDict):
    created: list[dict]
    duplicates: list[dict]
    success: bool
    error: Optional[str]


class AgentState(TypedDict):
    # Request
    request_id: str
    instruction: str
    raw_file_content: str
    file_name: str

    # Processing
    enriched_task: Optional[EnrichedTask]
    accuracy_definition: Optional[RAGResult]
    parsed_issues: list[ParsedIssue]
    classified_issues: list[ClassifiedIssue]
    accuracy_issues: list[ClassifiedIssue]

    # Orchestration
    slack_query: Optional[str]
    jira_query: Optional[str]

    # Agent results
    slack_result: Optional[SlackResult]
    jira_result: Optional[JiraResult]

    # Output
    errors: list[dict]
    metrics: dict
    trace_id: str
