# EXP-0005: Recoverable context and deterministic tool flow

**Status:** draft-1, planned and not preregistered. No provider calls or experimental results. See [manifest](manifest.json) and [HYP-0005](../../research/HYP-0005.md).

## Question and scope

Do recoverable evidence projections and bounded, already-authorized tool sequences improve independently checked outcomes per measured resource for the same native LLM harness? This is not a reproduction of HELIX and does not claim its savings transfer to this project.

## Instrument gate

Before inference, demonstrate task/evaluator binding, independent protected acceptance, deterministic record recovery, enforceable scope/budgets, and the [context contract](../../docs/context-evidence.md). Use fake adapters and failure injection. A receipt must name an actually recoverable authorized artifact; retrieval must not repeat the original operation.

Pin a real adapter capability profile. Apply the treatment only to supported tools/context surfaces. Record native tools/history outside that control. Do not pretend an MCP installation rewrites the complete conversation. Unsupported treatment conditions block the run.

## Four primary arms

| Arm | Context policy | Mechanical execution |
| --- | --- | --- |
| B0 | Native behavior with ordinary full tool evidence and bounded retrieval | Native worker coordination |
| R | Recoverable typed receipts and progressive exact retrieval | Same native worker coordination |
| D | Same context policy as B0 | Declared bounded deterministic sequences |
| RD | Same receipt policy as R | Same deterministic sequences as D |

All arms share the same underlying evidence access, model/harness/configuration, user task, safety controls, acceptance logic, and resource limits. The difference is representation or coordination, not privileged hidden answers or extra capabilities. Evidence retained solely for evaluation is not silently exposed as agent memory.

An optional cache-stable versus eager-replacement comparison is a subsequent registered ablation. Graph memory, vectors, skill induction, and extra reviewers are not bundled into this first comparison. Later M/P/MP experiments must declare their common context policy and retain a contemporary untreated control.

## Two separate workload regimes

**Fresh-task:** reset the native session between independent tasks. No cross-arm memories or learned procedures. Task families and held-out recombinations test transfer without historical carryover.

**Sequential:** run a declared sequence with retained context and permitted state. Repeat entire sequences independently, vary/block order prospectively, and treat a session/sequence as the analysis cluster. Fifty dependent items in one conversation are not fifty independent replicated sessions.

Report the regimes separately. Historical long-session savings do not establish benefits for fresh tasks. Record task order, resets/resumes, retained state, context thresholds, native compaction, and available cache observations.

## Cases that can falsify the mechanism

Include sparse but decisive errors inside large logs, misleading similarities, contradictory evidence, changed goals/dependencies, report selection changes, zero-test runs, delayed responses, uncertain mutations, unreadable/corrupt originals, permission revocation, and instruction-bearing source text.

Keep development and holdout families separate. Test evidence discovery without giving away the exact decisive handle. Evaluate the final candidate using protected criteria, not the receipt's summary. Positive/gold and negative controls qualify the evaluator without leaking solutions to workers.

## Measurement and accounting

Primary outcomes are verified task success and critical policy violations. Publish per-task outcomes, both-solve/neither-solve/each-only overlap, rejected/incomplete attempts, and uncertainty appropriate to the regime.

Secondary outcomes include all-attempt requests, input/cache/output usage, provider-defined reasoning subsets, unknown usage, observed price where available, wall time, retrieval calls, time to decisive evidence, artifact/index bytes, context prefix churn, checks, failed work, and maintenance.

Known tokens are subtotals when usage is missing. Record missing requests and explicitly unavailable costs. Do not add cached input to a total that already includes it, or reasoning to output that already includes it. Account for cache-write/read semantics using pinned provider documentation. Subscription quota and remote energy remain unknown unless actually observed.

Preserve primary and all-attempt ledgers. Predeclare any symmetric infrastructure exclusions and show their effect. Do not remove hard tasks, failed repairs, retrieval, finalization, or parent coordination to manufacture savings. A complete cost-per-success claim requires complete relevant cost accounting and a quality-qualified comparison.

## Analysis and decision rule

For a specified outcome Y, the factorial interaction is `Y(RD) - Y(R) - Y(D) + Y(B0)`. Analyze quality and costs separately. Matched repeated comparisons and intervals must respect family/session dependencies. No statistical significance or parity is inferred from the HELIX aggregate totals.

Before confirmatory execution, select the maximum acceptable quality loss, material resource improvement, sample size/power rationale, repetitions, analysis method, budget, stopping rule, missing-data policy, and review boundary. A small feasibility pilot cannot establish small gains or equivalence. Pilot-informed tasks become development data.

A candidate may be cheaper but lower-quality: report that trade-off and do not label it parity. Failure to detect a difference is insufficient for a noninferiority claim. Critical failures trigger the declared safety stop and remain in the report.

## Freeze blockers and authorization

Task generator/split, evaluator, pinned installed model/harness, treatment implementation, actual controls, seed/order schedule, repeat count, quality margin, cost definition, budgets, retention/access policy, and analysis are unresolved. The manifest sets paid spend to zero and provider execution unauthorized. This document does not create permission for installations, inference purchases, credential access, deployments, or private-memory import.

## Reproduction package

Preserve identities for task, candidate, protocol, evaluator, inputs, environment, and analysis; sanitized per-task rows; raw usage receipts where permitted; effect/recovery traces; and access-controlled original evidence. Publish what is recoverable and what is not. Hashes of inaccessible files alone are not a reproducible execution package.
