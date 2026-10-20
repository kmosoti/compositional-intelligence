# Candidate architecture: LLM-assisted compositional agent

**Status:** implementation design, not an implemented runtime or scientifically adopted architecture. See [ADR 0004](adr/0004-llm-assisted-research-instrument.md). Research can replace any mechanism; per-run contracts remain fixed only for interpretable comparisons.

## Objective and boundary

One persistent agent uses replaceable LLM harnesses for interpretation, candidate generation, code, and unfamiliar composition. Its authoritative state is outside any model conversation:

`AgentState = (TaskContract, Evidence, Claims, WorkGraph, Skills, ResourceLedger)`

The model sees a bounded, versioned projection. A new session or model does not reset the task's permissions, evidence identities, budget, or unresolved effects.

| Component | Responsibility | Boundary |
| --- | --- | --- |
| Task contract | Goal revision, scope, constraints, permitted effects, completion criteria | Retrieved text cannot amend it |
| Evidence store | Observations, source artifacts, provenance, retention state | Hash identity is not truth or authority |
| Claim store | Interpretations, assumptions, counterevidence, validity | Model assertions are not observations |
| Work board | Proposed observations, actions, dependencies, alternatives | A signal is not execution authorization |
| LLM workers | Interpretation and candidate generation | Cannot certify themselves or alter protected evaluation |
| Procedure library | Bounded reusable behavior with applicability contracts | Admission requires separate evidence |
| Trusted runtime | Scheduling, capabilities, budgets, effects, lifecycle | Enforced outside prompts |
| Evaluator | Exact-candidate checks using protected criteria | Engineering acceptance is not scientific adoption |

These are behavioral contracts, not a required microservice or crate per row. Prefer black-box interfaces with observable inputs, outputs, errors, and invariants.

## Representation portfolio

Use immutable evidence identities across raw artifacts, typed graph relations, lexical indexes, optional embeddings, and procedures. They are views, not independent competing copies of the truth.

Start with ordinary local indexed records, bounded graph traversal, and exact/lexical retrieval. A dedicated graph database is not necessary. Optional embeddings declare encoder version, dimensions, normalization, metric, and source identity; incompatible spaces are not silently mixed. Similarity proposes relevance, not applicability or permission.

Suggested relationships include `supports`, `contradicts`, `depends_on`, `derived_from`, `observed_in`, `applies_to`, `supersedes`, and `evaluated_by`. Causal claims remain distinct from operational dependencies. Do not materialize a universal logical closure.

Raw observations remain authoritative for what was observed. They do not necessarily describe the current world. Record collection time separately from source time and source revision. Dependency changes trigger reassessment, not historical deletion.

## Learning and execution loop

1. Bind the task to its authorized revision, starting snapshot, protected scope, and budget.
2. Observe the environment; retrieve relevant evidence, counterevidence, and compatible procedures.
3. Execute already-authorized exact work where its conditions hold.
4. Ask an LLM for an unfamiliar composition or a discriminating observation where needed.
5. Record outcomes, preserve alternatives, and invalidate affected assumptions.
6. Submit the exact candidate to protected evaluation.
7. Record the scoped result; integrate only through authorized controller logic.
8. Separately propose reusable procedures or representation changes for evaluation.

Routine work does not require an essay or multiple model calls. Request decisions, assumptions, predictions, and evidence references rather than private reasoning transcripts.

## Signals rather than a permanent LLM router

Components subscribe to new goals, missing evidence, conflicting claims, compatible skills, changed dependencies, failed checks, deadlines, and unsettled operations. They propose typed work items. A deterministic scheduler admits work according to capabilities, readiness, resource reservations, and bounded priorities.

Coalesce duplicate requests; bound fan-out, retries, queue growth, and dependency expansion. Do not poll a model to discover that nothing changed. Time, missing responses, and expiring evidence can also trigger work. Removing a permanent LLM manager does not remove the need for coordination.

## Records and contracts

**TaskContract:** task ID/revision, goal, starting snapshot, mutable/protected scope, tools/effects, acceptance identity, budget, stopping conditions.

**Observation:** artifact identity and location, source and resource versions, collection context, time, trust domain, sensitivity, retention/access state.

**Claim:** proposition, kind, scope, supporting/counterevidence, assumptions, proposer or derivation, invalidation conditions.

**WorkItem:** operation, task revision, dependencies, required capabilities, expected observation/artifact, resource scope, reservation, deadline, lifecycle.

**SkillContract:** typed inputs/outputs, preconditions, postconditions, effects, dependencies, implementation version, compatibility, evaluations, invalidation, measured or explicitly estimated cost.

A Markdown instruction skill and executable program are different artifact types. Candidate, evaluated, admitted, suspended, revised, and retired are distinct skill states. A single successful task does not justify universal applicability.

## Context and mechanical work

The [context-evidence contract](context-evidence.md) defines recoverable receipts and active-evidence protection. A compact receipt is a partial observation, not a semantically lossless substitute. A byte-perfect archive is insufficient if the agent cannot discover or interpret the needed evidence.

A deterministic sequence executes decisions already made within a bounded contract. It checks scope, inputs, artifact bindings, effects, stop conditions, and preconditions. It does not infer new goals or improvise semantic repairs. Environmental change returns control to decision-making. Reading an archive must never repeat the operation that produced it.

## Wider dimensions made operational

| Dimension | Candidate mechanism or test |
| --- | --- |
| Goal dependence | Multiple task-specific views; goal changes invalidate acceptance |
| Active observation | Choose experiments that separate explanations |
| Environmental co-design | Authorized fixtures, instrumentation, indexes, and tools |
| Temporal organization | Deadlines, validity horizons, versions, delayed effects |
| Plasticity | Revise/split/suspend procedures; preserve counterexamples |
| Culture | Transfer evaluated artifacts rather than entire conversations |
| Collective computation | Optional independently scoped reviewer or worker, with counted costs |
| Robustness | Restart, stale evidence, corruption, and unresolved-effect tests |
| Physical cost | Measure local work/storage separately from unobserved remote compute |
| Metacognition | Learn from measured errors/costs; do not equate self-confidence with calibration |

Retain alternative families: executable-model learning, direct adaptive control, agent-environment co-design, developmental/collective learning. Hyperdimensional representations, world models, local learning, and architecture search need their own discriminating experiments, not mandatory slots in the first build.

## Initial storage and adapters

Use local SQLite operational records and rebuildable indexes with content-addressed artifact files as the first candidate. Keep one controller-owned writer. Do not use a shared network-filesystem database as a distributed coordination mechanism. Rust hosts contracts and supervision; Python may support analysis.

Separate a proposal backend (no mutation authority) from a native worker backend (a bounded agent episode). Native episodes can contain many model requests and operations. The [runtime contract](agent-harness.md) covers lifecycle, isolation, supported controls, and accounting.

## Falsifiers

Equivalent-evidence lexical retrieval may beat graph expansion; vectors may select inapplicable analogies; skill overhead may exceed reuse savings; direct control may beat detailed modeling; multiple workers may duplicate errors. Reject or narrow components when their gains disappear under matched resources, unseen task families, changed goals, or complete accounting.

The native baseline is allowed to win. No brain analogy, code structure, or architectural diagram overrides that result.
