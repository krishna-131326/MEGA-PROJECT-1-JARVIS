# Security Audit

## Scope and method

Reviewed all first-party source, tracked-file inventory, Git history/statistics,
configuration absence, and committed dependency metadata. Runtime and live API testing
were not possible because no usable Python runtime exists.

## Findings

### SEC-01 — committed API credential (Critical)

**FACT:** the same NewsAPI key is hardcoded in `main.py:16`, `mine.py:19`, and
`gpt_enhanced.py:19`, and therefore exists in Git history.

**RISK:** unauthorized quota consumption and attribution to the owner. Removing the
working-tree string does not remove historical exposure.

**RECOMMENDATION:** revoke/rotate immediately; use `NEWS_API_KEY` from the environment;
add `.env`, `.venv`, caches, and credentials to `.gitignore`; enable secret scanning.
If history rewriting is chosen, coordinate it because commit IDs and clones change.

### SEC-02 — secret in query string (High)

**FACT:** NewsAPI authentication is interpolated into the request URL.

**RISK:** URLs are commonly captured by proxies, exception text, and access logs.

**RECOMMENDATION:** follow the provider-supported header mechanism, configure a timeout,
and redact credentials from all diagnostics.

### SEC-03 — unrestricted future tool execution boundary (High)

**FACT:** current browser actions use fixed destinations and user-derived Bing query
text. No shell execution exists. The proposed LLM does not yet exist.

**RISK:** adding LLM tool calling directly to current functions would allow untrusted
model output to drive OS/network side effects without schema validation, authorization,
or confirmation.

**RECOMMENDATION:** define typed tool schemas, strict allowlists, per-tool risk levels,
confirmation gates, timeouts, output limits, and an append-only redacted audit trail.
Never expose arbitrary `eval`, `exec`, or shell as a general assistant tool.

### SEC-04 — dependency provenance and patching failure (High)

**FACT:** a full virtual environment and executable binaries are committed. There is no
lockfile or declared direct dependency list.

**RISK:** reviewers cannot distinguish intended direct dependencies from transitive
artifacts; binary provenance and reproducibility are unverifiable; security updates
cannot be managed normally.

**RECOMMENDATION:** remove `.venv` and bytecode from tracking; declare direct
dependencies and hashes/lock resolution; run dependency and static-security scans in CI.

### SEC-05 — external data handling undefined (Medium)

**FACT:** recognized speech is sent to Google recognition and news is fetched from
NewsAPI. There is no privacy notice, retention policy, consent control, or log-redaction
policy.

**RISK:** users may not understand which audio/text leaves the machine. Future LLM memory
could persist sensitive conversations indefinitely.

**RECOMMENDATION:** disclose each processor, make cloud features opt-in, minimize data,
define retention/deletion controls, and keep memory disabled by default.

### SEC-06 — denial-of-service and reliability controls absent (Medium)

**FACT:** the NewsAPI request has no timeout. Playback and TTS are blocking. The process
uses an unbounded loop.

**RISK:** a stalled dependency can freeze the assistant; repeated failures can create a
tight noisy loop.

**RECOMMENDATION:** bounded timeouts, cancellation, retry only for transient/idempotent
operations with jitter and caps, circuit breaking, graceful shutdown, and rate limits.

## OWASP alignment

These findings map most directly to OWASP principles for cryptographic/secrets failures,
security misconfiguration, vulnerable/outdated components, identification of untrusted
inputs, and logging/monitoring failures. This is a design mapping, not a claim of OWASP
certification.

## Not found

**FACT:** no `subprocess`, `os.system`, `eval`, `exec`, database query, inbound HTTP
endpoint, authentication implementation, or uploaded-file handler exists in first-party
code.  
**INSUFFICIENT EVIDENCE:** absence of leaked secrets outside reviewed tracked content,
validity of the exposed key, dependency CVE status as of audit time, or transport
behavior during execution.

