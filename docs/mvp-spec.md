# MVP specification: one complete permission-boundary assessment

## Objective

Run local, reproducible checks against a demonstration AI agent and produce findings that a developer or small organization can understand.

## Planned inputs

- Principal identity and role.
- Synthetic documents with access labels.
- Explicit allow/deny authorization policy.
- Test cases describing expected access decisions.
- A local demonstration agent and simulated retrieval tool.

## Acceptance criteria

1. A clean installation can run the demo without external credentials.
2. Authorized access succeeds and unauthorized access is blocked by the tool.
3. At least one lower-trust instruction attempt is exercised and recorded.
4. Results contain the test ID, expected outcome, observed outcome, evidence, and remediation.
5. Reports are available in JSON and in a readable terminal format.
6. Automated tests verify both success and failure cases.

## Proposed finding format

```json
{
  "test_id": "AUTH-002",
  "status": "pass",
  "principal": "volunteer",
  "resource": "restricted-record-001",
  "expected_access": "denied",
  "observed_access": "denied",
  "evidence": [],
  "recommendation": "Enforce authorization within every data-access tool."
}
```

This is an illustrative schema, not output from an implemented tool.

## Non-goals

A universal prompt-injection detector, enterprise security dashboard, automated exploitation, or formal proof of safety.
