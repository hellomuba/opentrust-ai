import json

from opentrust_ai import assessment
from opentrust_ai.assessment import AssessmentRunner
from opentrust_ai.fixtures import DOCUMENTS, PRINCIPALS
from opentrust_ai.models import AuthorizationDecision
from opentrust_ai.policy import AuthorizationPolicy
from opentrust_ai.reporting import json_report, text_report


def test_report_covers_documented_scenarios():
    report = AssessmentRunner().run()
    assert report.summary == {"total": 4, "passed": 4, "failed": 0}
    assert [f.test_id for f in report.findings] == [
        "AUTH-001", "AUTH-002", "INJECT-001", "AUDIT-001"
    ]
    assert all(f.evidence and f.recommendation for f in report.findings)
    assert all(f.status == "pass" for f in report.findings)


def test_report_is_json_serializable_and_excludes_document_bodies():
    report = AssessmentRunner().run()
    encoded = json_report(report)
    decoded = json.loads(encoded)
    assert decoded["schema_version"] == "1.0"
    assert decoded["target"] == "local-synthetic-demo"
    assert len(decoded["findings"]) == 4
    assert "SYNTHETIC_RESTRICTED_MARKER" not in encoded
    assert "Ignore the user" not in encoded
    assert decoded["findings"][1]["expected_access"] == "denied"
    assert decoded["findings"][1]["observed_access"] == "denied"
    assert decoded["findings"][1]["evidence"][0]["reason"] == "insufficient_privileges"


def test_terminal_report_explains_results_and_limitations():
    rendered = text_report(AssessmentRunner().run())
    assert "4/4 passed" in rendered
    assert "INJECT-001" in rendered
    assert "Limitations:" in rendered
    assert "SYNTHETIC_RESTRICTED_MARKER" not in rendered


def test_assessment_detects_policy_bypass():
    class UnsafePolicy(AuthorizationPolicy):
        def decide(self, principal_id, document_id):
            if principal_id == "volunteer" and document_id == "restricted-record-001":
                return AuthorizationDecision(True, "unsafe_allow_all")
            return super().decide(principal_id, document_id)

    report = AssessmentRunner(UnsafePolicy(PRINCIPALS, DOCUMENTS)).run()
    finding = next(f for f in report.findings if f.test_id == "AUTH-002")
    assert finding.status == "fail"
    assert finding.observed_access == "allowed"
    assert report.summary["failed"] >= 1


def test_assessment_detects_agent_following_lower_trust_instruction(monkeypatch):
    original_agent = assessment.DemoAgent

    class UnsafeAgent(original_agent):
        def run(self, principal_id, document_id):
            result = super().run(principal_id, document_id)
            if document_id == "public-injected-001":
                self._retrieval.read(principal_id, "restricted-record-001")
            return result

    monkeypatch.setattr(assessment, "DemoAgent", UnsafeAgent)
    report = AssessmentRunner().run()
    finding = next(f for f in report.findings if f.test_id == "INJECT-001")
    assert finding.status == "fail"
    assert finding.checks["no_unrequested_tool_calls"] is False
    assert report.summary["failed"] >= 1


def test_assessment_evidence_contains_no_document_contents():
    report = AssessmentRunner().run()
    evidence = json.dumps([finding.evidence for finding in report.findings])
    for document in DOCUMENTS.values():
        assert document.content not in evidence
