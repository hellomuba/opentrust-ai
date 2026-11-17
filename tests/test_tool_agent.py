import pytest

from opentrust_ai.agent import DemoAgent
from opentrust_ai.audit import AuditTrail
from opentrust_ai.fixtures import DOCUMENTS, PRINCIPALS
from opentrust_ai.policy import AuthorizationPolicy
from opentrust_ai.tool import DocumentRetrievalTool


def make_agent():
    audit = AuditTrail()
    tool = DocumentRetrievalTool(AuthorizationPolicy(PRINCIPALS, DOCUMENTS), DOCUMENTS, audit)
    return DemoAgent(tool), tool, audit


def test_authorized_retrieval_returns_content_and_audit():
    agent, _, audit = make_agent()
    response = agent.run("coordinator", "internal-plan-001")
    assert response.observed_access == "allowed"
    assert DOCUMENTS["internal-plan-001"].content in response.answer
    assert len(audit.events) == 1
    assert audit.events[0].decision == "allowed"


def test_unauthorized_retrieval_denied_without_content():
    agent, tool, audit = make_agent()
    response = agent.run("volunteer", "restricted-record-001")
    assert response.observed_access == "denied"
    assert response.answer == "Access denied."
    assert DOCUMENTS["restricted-record-001"].content not in response.answer
    assert tool.read("volunteer", "restricted-record-001").content is None
    assert [event.decision for event in audit.events] == ["denied", "denied"]
    assert audit.events[1].reason == "insufficient_privileges"


def test_prompt_injection_is_untrusted_data_not_an_instruction():
    agent, _, audit = make_agent()
    response = agent.run("volunteer", "public-injected-001")
    assert "Ignore the user" in response.answer
    assert DOCUMENTS["restricted-record-001"].content not in response.answer
    assert [event.resource for event in audit.events] == ["public-injected-001"]


def test_direct_attempt_to_follow_injection_still_denied_by_tool():
    _, tool, audit = make_agent()
    attempted = tool.read("volunteer", "restricted-record-001")
    assert not attempted.decision.allowed
    assert attempted.content is None
    assert audit.events[0].decision == "denied"


@pytest.mark.parametrize("identifier", ["", "bad\nlog", "a" * 65, "../../etc/passwd", "ADMIN"])
def test_invalid_or_log_injection_identifiers_rejected(identifier):
    _, tool, audit = make_agent()
    with pytest.raises(ValueError):
        tool.read("volunteer", identifier)
    with pytest.raises(ValueError):
        tool.read(identifier, "public-notice-001")
    assert audit.events == ()


def test_unknown_resource_is_denied_and_logged():
    _, tool, audit = make_agent()
    result = tool.read("volunteer", "unknown-resource")
    assert result.content is None
    assert result.decision.reason == "unknown_resource"
    assert audit.events[0].resource == "unknown-resource"
    assert audit.events[0].decision == "denied"
