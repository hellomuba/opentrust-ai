"""Default-deny, server-side RBAC for the fictional document store."""

from types import MappingProxyType
from typing import Mapping

from .models import AuthorizationDecision, Document, Principal

ROLE_PERMISSIONS: Mapping[str, frozenset[str]] = MappingProxyType(
    {
        "volunteer": frozenset({"public"}),
        "staff": frozenset({"public", "internal"}),
        "admin": frozenset({"public", "internal", "restricted"}),
    }
)


class AuthorizationPolicy:
    """Resolve principals from a trusted registry, never from request-supplied roles."""

    def __init__(
        self,
        principals: Mapping[str, Principal],
        documents: Mapping[str, Document],
    ) -> None:
        self._principals = principals
        self._documents = documents

    def decide(self, principal_id: str, document_id: str) -> AuthorizationDecision:
        principal = self._principals.get(principal_id)
        if principal is None:
            return AuthorizationDecision(False, "unknown_principal")
        document = self._documents.get(document_id)
        if document is None:
            return AuthorizationDecision(False, "unknown_resource")
        allowed_levels = ROLE_PERMISSIONS.get(principal.role, frozenset())
        if document.classification not in allowed_levels:
            return AuthorizationDecision(False, "insufficient_privileges")
        return AuthorizationDecision(True, "role_allows_classification")
