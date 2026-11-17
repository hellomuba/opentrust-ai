"""Small, framework-independent models for the local demonstration."""

from dataclasses import dataclass
from typing import Literal

AccessLevel = Literal["public", "internal", "restricted"]
AccessOutcome = Literal["allowed", "denied"]


@dataclass(frozen=True, slots=True)
class Document:
    document_id: str
    classification: AccessLevel
    content: str


@dataclass(frozen=True, slots=True)
class Principal:
    principal_id: str
    role: str


@dataclass(frozen=True, slots=True)
class AuthorizationDecision:
    allowed: bool
    reason: str

    @property
    def outcome(self) -> AccessOutcome:
        return "allowed" if self.allowed else "denied"


@dataclass(frozen=True, slots=True)
class AuditEvent:
    sequence: int
    principal: str
    resource: str
    action: str
    decision: AccessOutcome
    reason: str


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    decision: AuthorizationDecision
    content: str | None


@dataclass(frozen=True, slots=True)
class AgentResult:
    principal: str
    resource: str
    observed_access: AccessOutcome
    answer: str
