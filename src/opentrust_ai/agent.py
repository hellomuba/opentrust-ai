"""A deterministic demonstration agent, not an LLM-powered assistant."""

from .models import AgentResult
from .tool import DocumentRetrievalTool


class DemoAgent:
    """Read only the document explicitly requested by the caller.

    Retrieved document text is returned as untrusted data. It cannot issue tool
    calls or change the principal's identity. This is intentionally a narrow
    test harness, not evidence of resistance in arbitrary LLM agents.
    """

    def __init__(self, retrieval: DocumentRetrievalTool) -> None:
        self._retrieval = retrieval

    def run(self, principal_id: str, document_id: str) -> AgentResult:
        result = self._retrieval.read(principal_id, document_id)
        if not result.decision.allowed:
            answer = "Access denied."
        else:
            answer = "Document content (untrusted):\n" + (result.content or "")
        return AgentResult(
            principal=principal_id,
            resource=document_id,
            observed_access=result.decision.outcome,
            answer=answer,
        )
