# Implementation Roadmap

Effort assumes one developer. Each sprint ends with evidence (tests, CI artifact, or
documented run), not only code.

## Sprint 1 — critical repairs (3–5 days)

- Rotate the exposed key; add configuration validation, `.gitignore`, and secret scans.
- Resolve local/remote branch history deliberately.
- Remove generated environment/cache artifacts from tracking.
- Create `pyproject.toml`, lock dependencies, and document supported platforms.

Dependencies: owner rotates credential and chooses history strategy.  
Risks: force-push disruption; Windows audio build issues.  
Outcome: clean, installable source repository.

## Sprint 2 — refactoring (5–8 days)

- Capture current commands as tests.
- Create typed command/result models and adapter protocols.
- Extract deterministic routing and an application factory.
- Consolidate three scripts into one CLI with optional voice mode.

Dependencies: Sprint 1 runtime.  
Risks: undocumented behavior regression.  
Outcome: side-effect-free core with injected adapters.

## Sprint 3 — Grok integration (5–8 days)

- Implement provider contract, fake, xAI adapter, timeouts/retries, and streaming.
- Version prompts; add usage/cost metadata and contract tests.
- Keep xAI opt-in behind configuration.

Dependencies: core interfaces and valid `XAI_API_KEY`.  
Risks: API/model changes, cost, prompt injection.  
Outcome: verified conversational fallback without SDK coupling.

## Sprint 4 — plugin/tool system (6–10 days)

- Define typed tool manifest, registry, risk levels, and permission checks.
- Add news/browser/music as built-in tools.
- Add confirmation and redacted audit events; document plugin compatibility.

Dependencies: stable command/tool contracts.  
Risks: arbitrary-code loading; premature API freeze.  
Outcome: controlled extensibility, not unrestricted code execution.

## Sprint 5 — persistent memory (5–8 days)

- Define opt-in use cases and threat model.
- Add SQLite repository, migrations, retention, delete/export, and context limits.
- Test tenant/session isolation and untrusted retrieval handling.

Dependencies: privacy decisions and stable conversation model.  
Risks: sensitive-data retention and prompt injection.  
Outcome: inspectable, deletable local memory.

## Sprint 6 — testing/evaluation (5–10 days)

- Expand unit, contract, integration, and failure-injection suites.
- Add golden tool-routing evaluation and latency/cost benchmark harness.
- Set justified quality gates from measured baseline.

Dependencies: Sprints 2–5.  
Risks: brittle mocks or misleading coverage-only goals.  
Outcome: repeatable evidence of behavior and limitations.

## Sprint 7 — Docker (3–5 days)

- Containerize text/API mode with a multi-stage, non-root image and health check.
- Document why host voice/audio remains platform-specific.
- Verify build/run from a clean environment.

Dependencies: reproducible package and text mode.  
Risks: USB/audio passthrough complexity and image bloat.  
Outcome: portable non-voice demo/deployment.

## Sprint 8 — CI/CD (3–5 days)

- Add format, lint, type, unit/contract, secret, and dependency jobs.
- Build container and publish only on approved tags.
- Add branch protection guidance, provenance, and rollback procedure.

Dependencies: stable commands and tests.  
Risks: flaky hardware/network integration tests.  
Outcome: enforced quality and reproducible artifacts.

## Sprint 9 — documentation (3–5 days)

- Write README quickstart, architecture decision records, threat model, configuration,
  plugin guide, evaluation report, demo script, and limitations.
- Add contributing, security, code-of-conduct, and license files.

Dependencies: verified interfaces and release workflow.  
Risks: documentation drifting from code.  
Outcome: reviewer can install, understand, test, and evaluate the system.

## Sprint 10 — public release (3–5 days)

- Run clean-machine acceptance, security review, dependency/license audit, and demo.
- Resolve release blockers; tag a semantic version and publish CI-built artifacts.
- Create issues for measured limitations and gather user feedback.

Dependencies: all prior acceptance gates.  
Risks: leaked test data, unsupported claims, operational cost.  
Outcome: an evidence-backed first public release.

