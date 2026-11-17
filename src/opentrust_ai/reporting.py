"""Human-readable output without reproducing untrusted document contents."""

import json

from .assessment import AssessmentReport


def json_report(report: AssessmentReport) -> str:
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n"


def text_report(report: AssessmentReport) -> str:
    lines = [
        "OpenTrust AI | Synthetic demo security assessment",
        f"Target: {report.target}",
        f"Results: {report.summary['passed']}/{report.summary['total']} passed; "
        f"{report.summary['failed']} failed",
        "",
    ]
    for finding in report.findings:
        lines.extend(
            [
                f"[{finding.status.upper()}] {finding.test_id}: {finding.description}",
                f"  Principal: {finding.principal} | Resource: {finding.resource}",
                f"  Expected: {finding.expected_access} | Observed: {finding.observed_access}",
                f"  Checks: {', '.join(k for k, v in finding.checks.items() if not v) or 'all passed'}",
                f"  Recommendation: {finding.recommendation}",
                "",
            ]
        )
    lines.append("Limitations:")
    lines.extend(f"  - {item}" for item in report.limitations)
    return "\n".join(lines) + "\n"
