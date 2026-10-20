# Compositional Intelligence

**Use models for unfamiliar work. Preserve evidence. Test reusable mechanisms.**

A research project building a persistent agent around existing LLM harnesses, exact tools, evidence-linked memory, and independently evaluated procedures. The agent is an experimental instrument for investigating useful composition, transfer, adaptation, and capability under bounded resources. It is not a commitment to an LLM-centered theory of intelligence.

**Status: research infrastructure and design.** The repository contains instructions, minimal Rust types, templates, and offline consistency checks. It does not yet implement the proposed autonomous runtime, isolated evaluator, provider integrations, or context-evidence pipeline. No cognitive benefit or token saving has been demonstrated here. There are no alpha versions or release milestones.

## Current approach

Start with one persistent user-facing agent and one scoped native LLM worker. Keep task state, evidence, permissions, budgets, effects, and acceptance outside the model conversation. Use deterministic procedures for already-decided mechanical work; ask models to interpret, hypothesize, generate candidates, and handle unfamiliar composition.

The first workload is bounded software engineering and research experimentation. The first comparator is the **same pinned native harness with ordinary tools and normal context behavior**, not an intentionally weak model. Local small-model and non-LLM alternatives remain valid competitors; earlier experiment plans retain their original scope.

The research question is whether added mechanisms improve independently verified outcomes or lifecycle cost without unacceptable regressions. Minimizing tokens regardless of solved tasks is not the objective.

## What changes, and what does not

- Build a reliable single-task instrument before adding graph memory, executable skill acquisition, vector retrieval, or multiple workers.
- Treat recoverable context projections and bounded deterministic tool flow as separately testable mechanisms. Exact archives do not guarantee that the model finds or uses the right evidence.
- Use a shared work board and explicit event subscriptions, with deterministic admission and resource arbitration. No permanent LLM manager or fixed agent caste is required.
- Keep raw observations, hypotheses, derived claims, and evaluation verdicts distinct. Similarity is not truth; a successful command is not task acceptance.
- Preserve research-led revision: research, experiments, analysis, and renewed research govern direction. Current code and prior art are information, not oracles.

[ADR 0004](docs/adr/0004-llm-assisted-research-instrument.md) explains this owner-directed implementation priority and its alternatives. It does not claim scientific adoption of the candidate architecture.

## Start here

| Document | Purpose |
| --- | --- |
| [Research charter](docs/research-charter.md) | Scope, resources, and epistemic boundaries |
| [Research program](docs/research-program.md) | Broad questions and competing mechanism families |
| [Candidate architecture](docs/architecture.md) | Agent state, replaceable components, and representations |
| [Runtime contract](docs/agent-harness.md) | Authority, integration, lifecycle, effects, and recovery |
| [Context and evidence contract](docs/context-evidence.md) | Exact retention, partial receipts, retrieval, invalidation, and cache behavior |
| [Implementation sequence](docs/implementation-plan.md) | Small vertical slices and explicit acceptance gates |
| [HELIX assessment](docs/research/helix-context-review.md) | Source inspection, arithmetic, limits, and lessons worth testing |
| [EXP-0005](experiments/EXP-0005/protocol.md) | Draft context/tool-flow comparison; no execution claimed |
| [Scientific methodology](docs/methodology.md) | Experimental discipline |
| [Coordination contract](docs/coordination.md) | Existing manual operating procedure and review boundaries |
| [Agent instructions](AGENTS.md) | Vendor-neutral operating contract |

The [hypothesis registry](research/README.md), [experiment registry](experiments/README.md), [Krakauer review](docs/research/krakauer-intelligence.md), and [harness source review](docs/research/agent-harness-review.md) remain part of the broader investigation. EXP-0001 through EXP-0004 are preserved, not retroactively rewritten to support the new priority.

## Initial engineering choices

Rust is the current host-runtime starting point. Use local SQLite records and content-addressed artifacts before introducing database servers or distributed coordination. Integrate Codex first through a supported, version-pinned interface; add Pi or Claude only through explicit capability-checked adapters. These are implementation candidates, not necessary properties of intelligence.

Hosted inference, local computation, API charges, subscription quota, tokens, and energy have separate accounting boundaries. Do not infer quota savings or joules from token reductions. No silent paid-API fallback, deployment, unrestricted self-modification, or recursive worker spawning is authorized by this design.

## Development and records

```bash
cargo fmt --all --check
cargo test --workspace
cargo clippy --workspace --all-targets -- -D warnings
python scripts/check_research.py
```

Cargo packages use the unpublished placeholder version `0.0.0`. The [coordination record guide](harness/coordination/README.md) covers the existing offline checks and synthetic examples. Structural checks do not authenticate evidence or demonstrate cognitive performance.

Implementation, instrument acceptance, experimental outcome, and architectural adoption are separate states. Preserve negative results and unsuccessful attempts. A native worker saying it finished is not an evaluator accepting the exact candidate.

## Wiki and licensing

`wiki/` contains separately published Wiki sources. Updating this repository does not update the live GitHub Wiki. The repository retains its existing MIT license; external projects are cited, not vendored by this rewrite.
