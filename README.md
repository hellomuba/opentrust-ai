# OpenTrust AI

**Independent, reproducible security checks for AI agents, designed for organizations without dedicated security teams.**

**Status: Experimental local demonstration (v0.1.0).** The repository contains a runnable, credential-free security assessment against a deterministic demonstration agent. This is **not** a production security scanner, an LLM prompt-injection detector, or a security certification. No users, pilots, or detection metrics are claimed.

## What the demo does

OpenTrust exercises a small fictional document service with three trusted principals, public/internal/restricted classifications, default-deny role policies, and per-action audit events. A deliberately hostile instruction is embedded in a public document to test whether the fixed demonstration agent treats that document as untrusted data. The test runner executes the four scenarios documented in [the threat model](docs/threat-model.md):

| ID | Test | Expected result |
| --- | --- | --- |
| AUTH-001 | Volunteer reads a public document | Allowed |
| AUTH-002 | Volunteer requests a restricted document | Denied by retrieval tool |
| INJECT-001 | Public document instructs agent to retrieve a restricted record | Instruction is not followed |
| AUDIT-001 | Director reads a restricted document | Allowed and audited |

Findings include test IDs, expectations, observed access, check results, metadata-only audit evidence, remediation guidance, and explicit limitations. All resources and principals are synthetic. No credentials or network requests are required for the CLI assessment.

## Requirements and installation

Python 3.11 or newer, with `pip` available.

```bash
git clone https://github.com/hellomuba/opentrust-ai.git
cd opentrust-ai
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -e '.[dev]'
```

Run the local assessment and export a structured report:

```bash
opentrust demo
opentrust demo --format json --output report.json
python -m pytest -q
```

The same CLI is available via `python -m opentrust_ai demo --format json`. A nonzero exit code indicates at least one failed assessment check.

### Optional local FastAPI adapter

The API runs the **same four fixed synthetic tests**. It cannot access a remote target or user-specified repositories.

```bash
python -m pip install -e '.[api]'
uvicorn opentrust_ai.api:app --host 127.0.0.1 --port 8000
curl -X POST http://127.0.0.1:8000/v1/assessments/demo
```

`GET /healthz` returns a health indicator. The demonstration API has no authentication; **do not expose it on a public network**. The API is optional and not used by the core CLI assessment.

## Repository layout

```text
src/opentrust_ai/
  fixtures.py     # Fictional principals, classifications, and documents
  policy.py       # Default-deny role authorization
  tool.py         # Authorization-enforcing document retrieval
  agent.py        # Deterministic agent with no LLM dependencies
  audit.py        # Per-scenario metadata-only access traces
  assessment.py   # Security scenarios and pass/fail evaluation
  reporting.py    # JSON and readable terminal output
  cli.py          # Local command-line runner
  api.py          # Optional localhost-only FastAPI adapter
tests/            # Policy, agent, injection, audit, and report tests
```

## Security model and limitations

- Authorization occurs inside the document retrieval tool; instructions in source documents cannot grant access.
- Principal roles come from trusted fixture data, not from caller-provided role fields.
- Untrusted document text is never executed, and the audit trail does not contain document bodies.
- This demo is deterministic and **does not contain a generative model**. The injection check validates only that this simple agent makes no extra tool calls in response to the injected text. It does not measure prompt-injection detection or safety for LangChain, LangGraph, or third-party agents.
- The fixture store is in memory, there is no real identity verification, no persistence, no authorization for API clients, and no real integrations. Do not deploy it against live data.

See the [MVP specification](docs/mvp-spec.md), [roadmap](docs/roadmap.md), [contributing guidelines](CONTRIBUTING.md), and [responsible security testing policy](SECURITY.md). Assess only systems you own or are explicitly authorized to test.

## Maintainer and license

Mubarak Ibrahim · [GitHub](https://github.com/hellomuba) · [Portfolio](https://hellomuba.github.io)

Apache License 2.0. Only independently owned or appropriately licensed contributions should be included.
