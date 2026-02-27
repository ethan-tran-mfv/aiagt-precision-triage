from typing import TypedDict, Optional


class FilterCriteria(TypedDict):
    type: str            # "accuracy" | "performance" | "security" | "critical" | "custom"
    description: str     # natural language: what to look for in issues
    confidence_threshold: float


class EnrichedTask(TypedDict):
    intent: str                              # "query" | "filter_and_report" | "analyze" | "update"
    requires_file_processing: bool
    filter_criteria: Optional[FilterCriteria]
    requires_slack_post: bool
    requires_ticket_creation: bool
    requires_analysis: bool
    output_format: str                       # "executive" | "detailed" | "bullet"


class ParsedIssue(TypedDict):
    id: str
    title: str
    description: str
    steps: str
    severity: str


class ClassifiedIssue(TypedDict):
    issue_id: str
    matches_criteria: bool
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
    slack_url: Optional[str]
    success: bool
    error: Optional[str]


class JiraResult(TypedDict):
    created: list[dict]
    duplicates: list[dict]
    success: bool
    error: Optional[str]


class AnswerResult(TypedDict):
    answer: str
    sources: list[str]
    confidence: float


class AgentState(TypedDict):
    # Request
    request_id: str
    trace_id: str
    instruction: str
    raw_file_content: Optional[str]
    file_name: Optional[str]

    # Enrichment
    enriched_task: Optional[EnrichedTask]

    # RAG
    rag_context: Optional[RAGResult]

    # File processing
    parsed_issues: list[ParsedIssue]
    classified_issues: list[ClassifiedIssue]
    filtered_issues: list[dict]          # ClassifiedIssue or ParsedIssue depending on path

    # Orchestration
    slack_query: Optional[str]
    jira_query: Optional[str]
    answer_query: Optional[str]

    # Agent results
    slack_result: Optional[SlackResult]
    jira_result: Optional[JiraResult]
    answer_result: Optional[AnswerResult]

    # Output
    errors: list[dict]
    metrics: dict
