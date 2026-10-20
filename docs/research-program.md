# Research program: capability through testable composition

**Updated:** 2026-10-20. **Status:** research direction and planned instruments, not demonstrated cognitive benefits.

## Governing principle

Research -> experiments -> analysis -> renewed research governs technical direction. Code and prior art are information, not oracles. Freeze a comparison, not the future architecture. [ADR 0002](adr/0002-research-governs-implementation.md) remains the governance policy; [ADR 0004](adr/0004-llm-assisted-research-instrument.md) changes the immediate implementation priority.

## First instrument and central question

Build a persistent agent that uses existing LLM harnesses while keeping task state, evidence, permissions, budgets, effects, and evaluation outside the conversation. Can recoverable context, exact procedures, evidence-linked memory, and other mechanisms improve unfamiliar problem solving and lifecycle cost against a competitive native baseline?

Separate engineering success from research success. A reliable instrument can produce a negative result about graph memory. That is useful progress. The first implementation is not a declaration that LLMs or graphs are necessary for intelligence.

## Do not collapse the search space

Evaluate a system in context: architecture, environment, interfaces/actions, goals, developmental history, other agents, and resource budget. Observed outcomes are a vector, not a universal intelligence score.

| Dimension family | Intervention worth testing |
| --- | --- |
| Information and representation | Change encoding while preserving the task; compare equal-evidence views |
| Goals and relevance | Make a previously irrelevant distinction consequential |
| Observability and causality | Preserve passive correlations but change intervention outcomes |
| Control and embodiment | Compare detailed predictive modeling with direct feedback or a better interface |
| Temporal organization | Change delays, prediction horizon, or evidence freshness |
| Learning and credit assignment | Delay feedback or introduce interacting causes |
| Plasticity and development | Reorder experience and test later learning, not only current skill |
| Memory and recoverability | Corrupt a cache or remove a retrieval cue while preserving source evidence |
| Composition and analogy | Test unseen combinations and superficially similar counterexamples |
| Social organization and culture | Transfer artifacts, alter communication, or remove experienced members |
| Robustness and repair | Remove a component or introduce a common-mode failure |
| Physical realization | Count local data movement and resource costs; mark hidden provider compute unknown |
| Incentives and evaluation | Change the proxy, evaluator, or deployment distribution without changing nominal goals |
| Open-ended discovery | Introduce useful new distinctions rather than only compressing old ones |

These families interact and are not exhaustive or independent. Expand the map when a controlled contrast exposes an omitted explanatory factor. Do not create a software module for every noun.

## Competing solution families

Keep executable-model learning, adaptive dynamical control, agent-environment co-design, and developmental/collective learning in contention. Useful abstractions can be non-nested and task-specific. Efficient prediction may be unnecessary for a successful feedback controller. Extra redundancy may improve repair. Tool construction may be cheaper than repeated inference. The current LLM-assisted instrument makes some of these questions easier to test; it does not resolve them by definition.

The [Krakauer review](research/krakauer-intelligence.md) and [harness source review](research/agent-harness-review.md) provide distinct kinds of evidence. A cognitive theory does not prove process isolation; a cancellation implementation does not prove learned abstraction. [HELIX](research/helix-context-review.md) supplies a concrete context-management case with important quality and accounting limitations.

## Units of evaluation

Name whether the claim concerns a frozen model, controller/memory mechanism, complete model-harness-tool system, a human assisted by it, or a population across time. State what persists between tasks. System-level learning through memory or procedures is not a hosted-weight update. Information access, metacognition, conscious access, and subjective experience remain distinct questions.

## Preserved and new investigations

| Record | Question | Current standing |
| --- | --- | --- |
| [HYP-0001](../research/HYP-0001.md) / [EXP-0001](../experiments/EXP-0001/manifest.json) | Marginal utility and retrieval baseline | Original planned scaffold preserved |
| [HYP-0002](../research/HYP-0002.md) / [EXP-0002](../experiments/EXP-0002/protocol.md) | Reusable abstraction and causal transfer | Planned; not superseded as a scientific question |
| [HYP-0003](../research/HYP-0003.md) / [EXP-0003](../experiments/EXP-0003/protocol.md) | Functional coordination | Planned; no consciousness claim |
| [HYP-0004](../research/HYP-0004.md) / [EXP-0004](../experiments/EXP-0004/protocol.md) | Human competence retained after assistance | Planned; separate learner and authorization boundary |
| [HYP-0005](../research/HYP-0005.md) / [EXP-0005](../experiments/EXP-0005/protocol.md) | Recoverable context and deterministic flow | New draft; first instrument-related comparison |

IDs are not release milestones or proof of execution. The [implementation sequence](implementation-plan.md) prioritizes instrument reliability, then isolated mechanisms. Later graph-memory/procedure factorial tests and vector/reviewer ablations require their own prospective protocols.

## Method and accounting

Use equivalent underlying evidence when comparing representations. Separate fresh per-task sessions from sequential work with retained state. A continuous conversation creates dependence and historical carryover: repeated whole sequences, not individual items treated as independent draws, are needed for relevant uncertainty estimates.

Measure verified success, per-task overlap/regressions, transfer, policy violations, attempts, requests, latency, memory, retrieval, and all visible costs. Account for acquisition, indexing, failed work, verification, and maintenance. Tokens, dollars, quota, host energy, and unobserved remote compute are different quantities. Keep missing usage explicitly unknown; do not double count provider-defined subsets.

Pin model/harness/configuration, task generator and split, evaluator, context policy, native compaction settings, exposure history, and access boundaries. Compare concurrent/interleaved contemporary controls where practical; retain historical comparisons as exploratory evidence. A component claim requires an ablation, not just a whole-product comparison.

Predeclare a material effect, a quality/noninferiority criterion where appropriate, sample-size rationale, missing-data policy, exclusions, budgets, and stopping rules. Failure to detect a difference is not evidence of equivalence. Pilot data that guided development are no longer unseen confirmatory evidence.

## What changes the direction?

Equivalent performance from a simpler representation weakens the case for added structure. Savings that disappear after retrieval or verification reject the apparent benefit. Regressions under changed goals or dependencies narrow a procedure's applicability. A rigid pipeline can beat adaptive coordination. Strong human unaided transfer can support an assistance policy even when immediate output is slower. Evidence corruption invalidates affected conclusions, not historical records.

Preserve negative results and maintain a distinction between implementation acceptance and scientific adoption. No finite task battery establishes general intelligence, brain-level efficiency, or superiority across unspecified environments.
