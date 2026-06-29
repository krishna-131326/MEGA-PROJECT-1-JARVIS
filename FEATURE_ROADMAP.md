# Feature Roadmap

Complexity uses S (≤2 days), M (3–7 days), L (1–3 weeks), assuming one developer and
excluding external review. Estimates are planning ranges, not commitments.

## P0 — critical repairs

| Feature | Why / resume impact | Complexity | Dependencies / steps | Risks |
|---|---|---:|---|---|
| Rotate secret and clean config | Prevents immediate abuse; baseline professionalism | S | Revoke key; env settings; redaction; secret scan | history still contains key |
| Reproducible package | Makes any claim testable | M | `pyproject`; lock; `.gitignore`; clean venv; supported Python matrix | audio wheels vary by OS |
| Deterministic core | Enables tests and safe evolution | M | typed commands/results; injected ports; one entry point | behavior changes during dedupe |
| Baseline tests/CI | Creates verifiable evidence | M | router/error tests; lint/type/test workflow | hardware paths need fakes |

## P1 — production foundations

| Feature | Why / resume impact | Complexity | Dependencies / steps | Risks |
|---|---|---:|---|---|
| Structured configuration/logging | Operability and secret hygiene | M | settings validation; JSON logs; correlation/redaction | accidental content logging |
| Resilient adapters | Prevent hangs and classify failures | M | timeouts; bounded retry; cancellation; circuit state | retry storms |
| CLI text mode | CI/demo path independent of hardware | S | input/output adapters; graceful shutdown | feature drift from voice |
| Containerized text/API mode | Reproducible demo | M | multi-stage image; non-root user; health check | host audio is not portable |

## P2 — resume-enhancing capabilities

| Feature | Why / resume impact | Complexity | Dependencies / steps | Risks |
|---|---|---:|---|---|
| Provider-neutral LLM adapter | Demonstrates architecture, not SDK glue | L | contracts; xAI adapter; fake adapter; contract tests | API churn/cost |
| Permissioned tool registry | Core assistant safety story | L | schemas; validation; risk labels; confirmation/audit | prompt injection |
| Evaluation harness | Quantifies quality | L | golden command set; tool accuracy; latency/cost reports | overfitting fixtures |
| Plugin SDK v1 | Extensibility with boundaries | L | stable tool contract; discovery; version compatibility | premature abstraction |

## P3 — advanced AI

| Feature | Why / resume impact | Complexity | Dependencies / steps | Risks |
|---|---|---:|---|---|
| Opt-in memory | Useful continuity with privacy controls | L | SQLite; retention; delete/export; retrieval tests | sensitive data leakage |
| Streaming/cancellation | Better interaction latency | M | async event model; TTS chunk policy | race/backpressure bugs |
| Human-approved workflows | Safe multi-step execution | L | state machine/checkpoints; resumability | stale approvals |
| Local provider | Privacy/offline fallback | L | hardware detection; OpenAI-compatible adapter; benchmarks | poor model/tool quality |

## P4 — research, only with evidence

- Durable workflow orchestration when multi-step resumability becomes a real use case.
- RAG when a defined private corpus and evaluation set exist.
- Multi-agent collaboration only if a single-agent baseline demonstrably fails.
- Multimodal input after privacy, storage, and evaluation requirements are defined.

## Ideas extracted from current systems

Proven patterns worth adopting selectively are provider protocols and local backends
(Open WebUI), confirmation/sandboxing for code execution (Open Interpreter), durable
execution and human intervention (LangGraph), typed tools (PydanticAI), and explicit
state/tool abstractions (AutoGen). These are patterns, not dependencies we automatically
need.

Sources: [Open Interpreter](https://github.com/OpenInterpreter/open-interpreter),
[OpenHands](https://github.com/OpenHands/OpenHands),
[Continue](https://github.com/continuedev/continue),
[Open WebUI](https://github.com/open-webui/open-webui),
[LangGraph](https://docs.langchain.com/oss/python/langgraph/overview),
[AutoGen](https://microsoft.github.io/autogen/stable/index.html),
[PydanticAI](https://ai.pydantic.dev/).

**INSUFFICIENT EVIDENCE:** a repository-specific reason to adopt CrewAI, AutoGen,
LangGraph, or any other agent framework today. Plain Python protocols and a small state
machine are sufficient for the first target.

