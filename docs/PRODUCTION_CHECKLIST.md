# Production Checklist

Unchecked means not evidenced in this repository.

## P0 release blockers

- [ ] NewsAPI key revoked/rotated and removed from code/history plan
- [ ] `.venv`, bytecode, and editor artifacts removed from tracking
- [ ] `.gitignore` and `.env.example` added without real secrets
- [ ] direct dependencies declared and reproducibly locked
- [ ] supported Python/OS matrix documented
- [ ] clean-machine installation verified
- [ ] one canonical entry point
- [ ] unit tests cover parser/router and all failure branches
- [ ] CI runs format, lint, type, test, secret, and dependency checks

## Application behavior

- [ ] text mode works without microphone/audio hardware
- [ ] voice adapters fail gracefully and can be disabled
- [ ] network calls have deadlines and bounded retry policies
- [ ] unknown/ambiguous commands return typed, useful results
- [ ] graceful shutdown and resource cleanup verified
- [ ] browser/audio side effects are injectable and testable
- [ ] no import-time hardware initialization

## Security and privacy

- [ ] secrets sourced from a secret manager/environment and redacted
- [ ] tool schemas validate all model/user inputs
- [ ] consequential tools require explicit confirmation
- [ ] allowlists and least privilege applied
- [ ] prompt-injection threat model documented and tested
- [ ] conversation retention, export, and deletion policies implemented
- [ ] cloud speech/LLM processors disclosed and opt-in where appropriate
- [ ] security policy and vulnerability-reporting path published

## LLM quality

- [ ] provider-neutral contract and deterministic fake exist
- [ ] pinned model used for evaluated flows
- [ ] tool-call and fallback contract tests pass
- [ ] golden evaluation dataset versioned
- [ ] accuracy, latency, and cost measured from actual runs
- [ ] fallback cannot duplicate side effects

## Operations and release

- [ ] structured redacted logs with correlation IDs
- [ ] health/readiness behavior defined
- [ ] metrics for errors, latency, retries, tokens, and costs
- [ ] container runs as non-root with minimal image
- [ ] configuration documented by environment
- [ ] backup/restore tested if memory is enabled
- [ ] dependency updates and rollback procedure documented
- [ ] README quickstart, architecture, demo, limitations, and license present
- [ ] tagged release built from CI with changelog

## Current status

0 checklist items are verified by repository evidence. This does not mean every item is
equally urgent; complete P0 before marketing or feature expansion.

