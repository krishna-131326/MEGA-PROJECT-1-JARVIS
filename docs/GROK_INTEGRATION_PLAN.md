# Grok Integration Plan

## Decision

Choose **Option B: optional/fallback-capable provider**, initially enabled explicitly
rather than silently. Option A (primary) is premature because there is no LLM baseline,
contract suite, latency measurement, budget, or reliability evidence. Option C (coding
specialist) is outside the current assistant use case. Option D (research mode) may be a
later tool because xAI offers server-side search, but requires citations and cost tests.
Option E rejects a resource that can add real conversational/tool-selection value.

## Official capability evidence

xAI currently documents an OpenAI-compatible API endpoint, streaming, custom function
calling, built-in web/X search, rate limits returning HTTP 429, and model aliases versus
pinned releases. Current pricing is usage-based and must be read at deployment time:
[models](https://docs.x.ai/developers/models),
[function calling](https://docs.x.ai/developers/tools/function-calling),
[rate limits](https://docs.x.ai/developers/rate-limits),
[pricing](https://docs.x.ai/developers/pricing).

## Proposed layout

```text
jarvis/llm/
├── protocols.py             LLMProvider protocol and neutral value objects
├── errors.py                Auth, RateLimit, Timeout, InvalidResponse, Unavailable
├── router.py                explicit provider/fallback policy
├── prompts/
│   ├── assistant_v1.txt
│   └── tool_policy_v1.txt
└── providers/
    ├── xai.py               xAI SDK/OpenAI-compatible adapter
    ├── local.py             optional local compatible endpoint
    └── fake.py              deterministic tests
```

`fallback.py` should be policy in `router.py`, not a provider pretending to be a model.

## Contract

The neutral request includes messages, allowed tool definitions, prompt version,
timeout, and correlation ID. The response includes text/tool calls, provider/model,
finish reason, usage, and latency. Streaming yields typed deltas and a terminal usage
event. Provider SDK objects must not leak into core code.

## Failure policy

- Retry transient 429/5xx/timeouts with exponential backoff plus jitter, honoring
  server guidance, a small attempt cap, and an overall deadline.
- Never retry authentication, validation, or content-policy failures.
- Fallback only before side effects or from a recorded checkpoint; never replay a tool
  action implicitly.
- Make fallback visible in metadata/logs and configurable. A local provider is not
  automatically quality-equivalent.
- Pin model versions for evaluated workflows; use aliases only where automatic behavior
  change is acceptable.

## Tool calling

Grok may select tools but cannot execute them directly. Flow:

```text
model tool call → schema validation → policy/allowlist → user confirmation if needed
→ adapter execution with timeout → redacted result → model continuation
```

Start with read-only news/search and fixed browser navigation. Local file, process,
purchase, message, or credential tools require stronger authorization and sandboxing.

## Prompt and memory strategy

Store prompts as versioned files with tests and evaluation metadata. Keep policy in
code; do not rely on a system prompt as an authorization boundary. Send only the minimum
memory required, label retrieved content as untrusted, cap context, and provide
retention/delete/export controls. Never send API keys or raw logs to the model.

## Cost and observability

Record input/output/cached tokens, tool charges, model ID, latency, retries, and fallback
without recording raw private conversations by default. Enforce per-request token caps,
daily budget alerts, and an off switch. Pricing and model availability are time-varying;
read official xAI pages before release rather than embedding this audit’s numbers.

## Acceptance gates

1. Fake-provider unit tests and xAI contract tests pass.
2. Missing/invalid key failures are actionable and redacted.
3. Tool arguments are validated and unauthorized tools cannot execute.
4. Retry/fallback tests prove no duplicated side effects.
5. Evaluation compares deterministic routing vs LLM routing on a versioned fixture set.
6. Cost/latency budgets are documented from actual runs.

**UNKNOWN:** the owner’s key entitlements, live model availability for that account,
observed quality, latency, and spend. No live xAI request was authorized or possible.

