# Agent harness design

The repository provides process instructions, templates, and offline record checks. A trusted autonomous controller, isolated execution service, external evaluator, and GitHub Project writer have **not been implemented**. The [coordination contract](coordination.md) defines the current manual operating procedure and its enforcement limits.

The [DeepSeek Harness, Pi, and Codex source review](research/agent-harness-review.md) supplies concrete implementation evidence and candidate mechanisms. Those implementations are references for experiments, not mandatory dependencies or proof of cognitive capability. The [research program](research-program.md) separates reliability of the experimental instrument from the intelligence claims evaluated with it.

## Three authorities
- **Worker:** scoped modifications and evidence proposal.
- **Evaluator:** owner of frozen tests, scientific protocol and comparison baselines.
- **Controller:** permissions, budgets, task state transitions and integration.

A reviewer model can assist but cannot independently certify itself. Sandboxing must be enforced by OS/container boundaries, not a prompt or Git worktree alone.

## Task state
Proposed -> Investigating -> Authorized -> Implementing -> Submitted -> Evaluating -> {Accepted, Rejected}. Blocked is an orthogonal condition with an explicit unmet requirement. Cancellation and supersession are dispositions; accepted negative and inconclusive research can be completed work. Scientific adoption is a distinct research decision. See the [record format](../harness/coordination/examples/README.md) for exact transitions and task-kind rules.

## Required input
Goal, known starting state, mutable paths, protected paths, dependency assumptions, resources, expected failure conditions, permitted tools and independent acceptance method.

## Recovery
Preserve failed candidate diffs and raw logs. Distill negative constraints distinguishing observation from root-cause hypothesis; retry only inside a disposable controlled workspace. Default cap may be three attempts but isn't a scientific law.

Bind the record to the original task revision and submitted evidence identities. A new report or timestamp does not revive expired authority. Preserve uncertain external write outcomes across retries; confirmed worker termination does not establish that all earlier effects are settled. Offline checks validate the supplied records, not process liveness or resource fencing.

## Contract amendments
Test policy and interface changes must be separate, independently reviewed changes with rationale, counterexample and compatibility assessment.

## Cost-aware agent work
Measure tokens, tool calls, retries, wall-clock, and validated outcomes; use minimal context, relevant single skill, and deterministic checks before model review. No permanent specialist agent role is required.
