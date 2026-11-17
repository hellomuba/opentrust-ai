"""Minimal per-scenario audit trail that never records document bodies."""

from .models import AuditEvent, AuthorizationDecision


class AuditTrail:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record(
        self,
        principal: str,
        resource: str,
        action: str,
        decision: AuthorizationDecision,
    ) -> None:
        self._events.append(
            AuditEvent(
                sequence=len(self._events) + 1,
                principal=principal,
                resource=resource,
                action=action,
                decision=decision.outcome,
                reason=decision.reason,
            )
        )

    @property
    def events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)
