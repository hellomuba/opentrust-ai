# OpenTrust AI

**Independent security checks for AI agents, designed for organizations without dedicated security teams.**

OpenTrust is an early-stage, open-source initiative to help organizations understand what their AI agents can access, what actions they can take, and what can go wrong.

> **Project status: Pre-prototype.** This repository documents a planned project. The first working security checks, demonstration agent, and reports are not yet implemented. There are no claimed users, pilots, or validated detection metrics.

## The problem

An AI agent connected to an inbox, documents, or business APIs can do useful work, but it can also access restricted information or follow malicious instructions embedded in untrusted content. Smaller organizations often lack the time or expertise to independently test those risks.

OpenTrust aims to make practical security assessments **reproducible, understandable, and affordable**.

## Proposed first working release

1. A controlled example agent with synthetic public and restricted documents.
2. Permission-boundary tests for authorized and unauthorized requests.
3. A test scenario involving malicious instructions in an untrusted document.
4. An audit trace showing attempted tool actions and authorization decisions.
5. JSON findings and plain-language explanations, including suggested remediation steps.

Future work may include more attack scenarios, additional agent frameworks, and a community security-clinic model. These are intentions, not completed features.

## Intended users

Nonprofits, independent developers, technical volunteers, community institutions, and small businesses deploying AI agents without specialist security teams. Early user research is planned in Nigeria. No partnerships or deployments are claimed.

## Documentation

- [Threat model](docs/threat-model.md)
- [MVP specification](docs/mvp-spec.md)
- [Roadmap](docs/roadmap.md)
- [Contributing](CONTRIBUTING.md)
- [Responsible security testing](SECURITY.md)

## Proposed technology

Python, pytest, a local command-line test runner, structured JSON reports, and potentially FastAPI. LangGraph and LangChain adapters can be considered after an initial testing contract is validated. Final choices will follow implementation.

## Principles

- Test behavior, not marketing claims.
- Enforce access control in tools and APIs, not only in prompts.
- Use synthetic fixtures, not customer or employer data.
- Produce actionable findings with explicit limitations.
- Work openly and incorporate user feedback.

## Maintainer

**Mubarak Ibrahim** · [GitHub](https://github.com/hellomuba) · [Portfolio](https://hellomuba.github.io)

## License

[Apache License 2.0](LICENSE). Only independently owned or appropriately licensed contributions should be added.

**Disclaimer:** OpenTrust is not a security certification and cannot guarantee that a system is safe.
