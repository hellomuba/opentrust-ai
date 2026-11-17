import pytest

from opentrust_ai.fixtures import DOCUMENTS, PRINCIPALS
from opentrust_ai.policy import AuthorizationPolicy


@pytest.mark.parametrize(
    ("principal", "resource", "allowed", "reason"),
    [
        ("volunteer", "public-notice-001", True, "role_allows_classification"),
        ("volunteer", "internal-plan-001", False, "insufficient_privileges"),
        ("volunteer", "restricted-record-001", False, "insufficient_privileges"),
        ("coordinator", "internal-plan-001", True, "role_allows_classification"),
        ("coordinator", "restricted-record-001", False, "insufficient_privileges"),
        ("director", "restricted-record-001", True, "role_allows_classification"),
        ("unknown", "public-notice-001", False, "unknown_principal"),
        ("volunteer", "missing-document", False, "unknown_resource"),
    ],
)
def test_default_deny_policy(principal, resource, allowed, reason):
    decision = AuthorizationPolicy(PRINCIPALS, DOCUMENTS).decide(principal, resource)
    assert decision.allowed is allowed
    assert decision.reason == reason


def test_roles_are_resolved_by_trusted_registry():
    policy = AuthorizationPolicy(PRINCIPALS, DOCUMENTS)
    assert policy.decide("director", "restricted-record-001").allowed
    # Caller cannot elevate by embedding a role into its identity.
    assert not policy.decide("volunteer:admin", "restricted-record-001").allowed
