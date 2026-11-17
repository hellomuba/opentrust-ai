"""Document retrieval: the authorization boundary is the tool, not a prompt."""

import re
from typing import Mapping

from .audit import AuditTrail
from .models import Document, RetrievalResult
from .policy import AuthorizationPolicy

_IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9-]{0,63}\Z")


class DocumentRetrievalTool:
    def __init__(
        self,
        policy: AuthorizationPolicy,
        documents: Mapping[str, Document],
        audit: AuditTrail,
    ) -> None:
        self._policy = policy
        self._documents = documents
        self._audit = audit

    def read(self, principal_id: str, document_id: str) -> RetrievalResult:
        # Keep logs bounded and single-line, including for unknown identifiers.
        if not _IDENTIFIER.fullmatch(principal_id) or not _IDENTIFIER.fullmatch(document_id):
            raise ValueError("Principal and document identifiers must be simple, bounded slugs")

        decision = self._policy.decide(principal_id, document_id)
        self._audit.record(principal_id, document_id, "read_document", decision)
        if not decision.allowed:
            return RetrievalResult(decision=decision, content=None)
        # Fail closed if a custom policy erroneously allows a nonexistent document.
        document = self._documents.get(document_id)
        if document is None:
            raise RuntimeError("Policy allowed an unknown document")
        return RetrievalResult(decision=decision, content=document.content)
