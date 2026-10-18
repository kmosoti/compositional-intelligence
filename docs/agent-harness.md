# Agent harness design

The repository provides process instructions and templates. A trusted autonomous controller, isolated execution service and external evaluator have **not been implemented**.

## Three authorities
- **Worker:** scoped modifications and evidence proposal.
- **Evaluator:** owner of frozen tests, scientific protocol and comparison baselines.
- **Controller:** permissions, budgets, task state transitions and integration.

A reviewer model can assist but cannot independently certify itself. Sandboxing must be enforced by OS/container boundaries, not a prompt or Git worktree alone.

## Task state
Proposed -> Investigating -> Authorized -> Implementing -> Submitted -> Evaluating -> {Accepted, Rejected, Blocked}. Scientific adoption is a distinct research decision.

## Required input
Goal, known starting state, mutable paths, protected paths, dependency assumptions, resources, expected failure conditions, permitted tools and independent acceptance method.

## Recovery
Preserve failed candidate diffs and raw logs. Distill negative constraints distinguishing observation from root-cause hypothesis; retry only inside a disposable controlled workspace. Default cap may be three attempts but isn't a scientific law.

## Contract amendments
Test policy and interface changes must be separate, independently reviewed changes with rationale, counterexample and compatibility assessment.

## Cost-aware agent work
Measure tokens, tool calls, retries, wall-clock, and validated outcomes; use minimal context, relevant single skill, and deterministic checks before model review. No permanent specialist agent role is required.
