# Implementation sequence and acceptance gates

**Status:** planned work, not delivered capabilities or a release schedule. [ADR 0004](adr/0004-llm-assisted-research-instrument.md) defines the scope. Work may be reordered when a cheaper discriminating experiment is found.

## A. Trustworthy single-task instrument

Implement typed task/evidence/claim/effect/usage records, local persistence, artifacts, one fake worker, a disposable fixture, and a protected evaluator. Use existing coordination vocabulary rather than creating a second incompatible task-state machine.

Acceptance: exact-candidate binding; accepted-request versus completed-worker versus solved-task distinction; duplicate/out-of-order events; restart without reissuing effects; unresolved outcomes; shared budget reservation; scope enforcement; and evaluator protection.

Next integrate one installed, version-pinned Codex App Server. Discover capabilities and available models. Record actual native events and usage. No paid calls or installations are authorized by this planning document. Unsupported controls block affected experiments.

## B. Evidence-preserving context and exact work

Implement retained originals, typed partial receipts, read-only expansion, protected active context, explicit invalidation, and compatible report deltas. Keep a full-evidence path. Add bounded deterministic sequences only for already-authorized decisions, with preconditions and stop conditions.

Acceptance: the [context contract](context-evidence.md), including cold recovery and unavailable-artifact tests. Measure the same model/harness before and after each treatment. Use [EXP-0005](../experiments/EXP-0005/protocol.md) to distinguish receipts, tool flow, and their interaction. No savings target is an acceptance substitute.

## C. Memory and reusable procedures

Add claim/evidence separation, exact and lexical retrieval, bounded graph views, and skill contracts. Introduce a candidate -> tested -> independently evaluated -> admitted -> suspended/retired lifecycle. Record where learning occurs: system memory/procedures, not hosted model weights.

Compare B0, graph-memory M, executable-procedure P, and MP with equal underlying evidence and a fixed declared context policy. Register this subsequent comparison before execution. Preserve a contemporary untreated native baseline so cumulative changes do not hide regressions.

Acceptance: no stale acceptance after goal/dependency changes; failed procedure evidence retained; family-level held-out applicability checks; acquisition and maintenance included in cost.

## D. Controlled extensions

Only then compare optional semantic vectors, targeted observation selection, independent reviewers, additional provider adapters, environmental tool construction, or distributed execution. Each needs a concrete question, baseline, budget, and falsifier. Different providers are not automatically independent witnesses.

Treat hyperdimensional binding, new world models, developmental search, and local learning as research candidates rather than mandatory modules. Self-improvement can propose a runtime patch; it cannot modify the current protected evaluator or deploy itself.

## Definition of progress

| Claim | Required evidence |
| --- | --- |
| Documented | Inspectable contract or protocol |
| Implemented | Source and executable entry point |
| Instrument checked | Named tests actually executed with bounded conclusions |
| Experiment run | Frozen or explicitly exploratory run artifacts and accounting |
| Mechanism supported | Interpretable comparative results with uncertainty and counterevidence |
| Adopted | Separate scoped decision and rollback/invalidation conditions |

A larger codebase, more agents, or a lower token subtotal is not progress by itself. No alpha release is scheduled by these gates.
