# Scientific and engineering method

Use design-science research for artifacts, controlled evaluation for claims and contract-governed implementation for agent-produced code.

## Research cycle
Problem signature -> competitive baseline -> hypothesis and falsifier -> predeclared protocol -> candidate implementation -> independent run -> analysis and counterexamples -> adopt/reject/reframe.

## Pre-registration
Record task distribution, holdout strategy, leakage checks, competing methods, random seeds, resource budgets, sample size justification, primary/secondary metrics and termination criteria before interpreting scores.

## Outcome measures
Correctness / task completion, held-out transfer, calibrated confidence, end-to-end latency (TTFT and total), token throughput where relevant, GPU/CPU/RAM peak, energy estimates (with measurement limitations), total cost per correct task, reliability and failure recovery.

## Comparison rules
Compare equivalent task inputs, tool access, machine state, model warm/cold conditions and time/energy budgets. Change one mechanism at a time for attribution; run factorial interactions when combinations are the question. Record uncertainty and independent replications.

## Invalid shortcuts
Do not use benchmark contamination, private test exposure to code-generating agents, sole reliance on model-as-judge, surrogate metrics claimed as intelligence, or purported one-click formal proofs. Green tests prove only what the tests exercise.

## First baseline
Quantized small LLM + lexical/vector retrieval + deterministic tools; establish correctness and measured cost. Only then test a distinct embedding/reranking/graph/HDC/CLM mechanism.
