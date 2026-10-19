# Scientific and engineering method

Use design-science research for artifacts, controlled evaluation for claims and contract-governed implementation for agent-produced code.

## Research cycle
Problem signature -> competitive baseline -> hypothesis and falsifier -> predeclared protocol -> candidate implementation -> independent run -> analysis and counterexamples -> adopt/reject/reframe.

The cycle can change the problem representation and replace the implementation. Source code is an observation about one candidate, not a constraint on what future research may propose. Explore distinct mechanisms and credible null explanations before converging. See [research governance](adr/0002-research-governs-implementation.md).

## Pre-registration
Record task distribution, holdout strategy, leakage checks, competing methods, random seeds, resource budgets, sample size justification, primary/secondary metrics and termination criteria before interpreting scores.

An experiment file with unresolved choices remains planned and is not preregistered merely because it has an ID. A confirmatory run freezes those choices; a subsequent amendment gets a new version and rationale. Preserve prior outcomes. Do not silently change an evaluator or discard a failing candidate to preserve an architecture.

## Outcome measures
Correctness / task completion, held-out transfer, calibrated confidence, end-to-end latency (TTFT and total), token throughput where relevant, GPU/CPU/RAM peak, energy estimates (with measurement limitations), total cost per correct task, reliability and failure recovery.

## Comparison rules
Compare equivalent task inputs, tool access, machine state, model warm/cold conditions and time/energy budgets. Change one mechanism at a time for attribution; run factorial interactions when combinations are the question. Record uncertainty and independent replications.

## Invalid shortcuts
Do not use benchmark contamination, private test exposure to code-generating agents, sole reliance on model-as-judge, surrogate metrics claimed as intelligence, or purported one-click formal proofs. Green tests prove only what the tests exercise.

## First baseline
Quantized small LLM + lexical/vector retrieval + deterministic tools; establish correctness and measured cost. Only then test a distinct embedding/reranking/graph/HDC/CLM mechanism.

This is an initial comparator, not a permanent privileged architecture. The existing EXP-0001 isolates retrieval by comparing a tools-only baseline with a retrieval-enabled arm. New questions may require exact symbolic, lookup, single-model, or equal-budget independent-candidate controls. Distinguish controlled mechanism comparisons from comparisons of complete native configurations.
