# Agent harness and execution contract

**Status:** proposed runtime boundaries. Existing repository functionality is instructions, minimal types, and offline record checks. No autonomous controller, isolated evaluator, provider adapter, or GitHub Project writer is established by this document. Existing [manual coordination](coordination.md) remains in force.

## Three authorities

- Worker: scoped observations, candidate modifications, and evidence proposals.
- Evaluator: independently controlled acceptance checks and protected evaluation material.
- Controller: permissions, budgets, task state, effect admission, and integration.

Model review can contribute findings but cannot substitute for independent acceptance. Keep the existing task phase vocabulary; do not conflate worker lifecycle events with task phases. A completed negative experiment can be accepted research. A completed model turn is not a solved task.

## First vertical slice

`TaskContract -> observed disposable workspace -> context packet -> one native worker -> exact candidate -> protected evaluator -> evidence-linked result`

Start with fake adapters and deterministic fixtures before authorized provider calls. One write-capable worker per workspace; no recursive spawning. Three candidate attempts is a proposed pilot cap, not a scientific constant. Freeze concrete deadlines and resource limits before execution.

## Provider boundaries

Expose capability discovery, start, event observation, input submission, cancellation request, settlement inspection, artifact export, and usage observation. These are proposed internal operations, not claims of identical native APIs.

Separate proposal requests from native agent episodes. An episode can contain multiple generations, retries, tools, and continuations. Keep credentials outside model-visible state and worker-readable artifacts.

Codex is the first integration candidate through the documented App Server. Pin its installed version and generated schemas; discover available models rather than assuming account entitlement. Threads, turns, items, approval requests, and usage notifications have distinct meanings. Official sources: [App Server](https://developers.openai.com/codex/app-server/) and [integration architecture](https://openai.com/index/unlocking-the-codex-harness/), checked 2026-10-20.

Pi and Claude remain optional later adapters. Recheck their installed protocol, authentication terms, permissions, resumption, cancellation, and settlement semantics at integration time. An API key, a subscription login, and an SDK are not interchangeable entitlements. Never silently fall back to paid API access.

Declare whether the adapter can control tool schemas, tool-result projection, native history, compaction, process isolation, and effect interception. A tool installation is not proof that every native request passes through our context policy. Reject unsupported experimental conditions rather than silently approximating them. Keep provider-owned opaque protocol items intact; do not reconstruct hidden reasoning.

## Effects and recovery

Persist intent before dispatch. Track preparation, dispatch, observed response, verification, cancellation request, confirmed termination, and unresolved/reconciled effects separately. A timeout can mean `outcome_unknown`, not failure-before-execution.

Reconcile the target or use supported idempotency before retrying an uncertain mutation. Do not promise exactly-once external effects from a local ledger. Log replay rebuilds recorded state; it does not reissue commands or reproduce stochastic model calls.

On restart, inspect outstanding processes and provider sessions before admitting conflicting work. An expired local lease does not revoke a worker's external credentials. Initial enforcement requires process isolation and restricted effect access, not only cooperative flags.

## Security and acceptance

OS/container boundaries enforce filesystem, process, network, and credential restrictions. Worktrees are collaboration mechanisms, not security sandboxes. Protected evaluator inputs and logic are outside worker write scope. Candidate-generated tests do not replace acceptance checks.

Bind acceptance to task revision, candidate digest, protocol, evaluator, inputs, and environment. Goal or dependency changes require an applicability decision. A shell exit code of zero, missing tests, a partial report, or a shorter log cannot establish acceptance.

Tool outputs, webpages, source comments, archived memory, and evidence receipts remain untrusted content. They cannot modify goals, grant permissions, or weaken evaluation. Preserve failed patches and counterexamples within the authorized retention policy.

## Resource accounting

Reserve resources before admission. All worker/reviewer calls, retries, retrieval, filtering, skill construction, checks, and recovery count toward the relevant parent workload. Keep request counts distinct from attempts and task-level repairs.

Record input, cache read/write, output, and reasoning categories according to the pinned provider's schema. Subsets must not be added twice. Missing usage is unknown, not zero. Record actual charges separately from subscription quota observations and local measurements. Token counts do not establish energy or quota savings.

## Instrument acceptance gates

Use deterministic fixtures to test duplicate/out-of-order events, accepted-but-incomplete requests, continued native work after a low-level event, crash-after-dispatch, late responses, cancellation, budget races, stale evidence, protected-file edits, permission escalation, and missing adapter controls.

Test exact recovery from retained evidence after restart, including corrupted/unavailable artifacts, changed task revisions, zero-test reports, and incompatible report deltas. The [context contract](context-evidence.md) specifies projection requirements. None of these checks, even if passed, establishes a cognitive improvement.
