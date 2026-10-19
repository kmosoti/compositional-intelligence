# EXP-0003: Functional coordination and metacognitive control

**Status:** planned; not preregistered; not implemented or executed. **Hypothesis:** [HYP-0003](../../research/HYP-0003.md). **Record:** [manifest](manifest.json).

## Mechanisms and limits

Test local processing, selective sharing, and computation allocation separately. A local module can be deterministic, probabilistic, neural, or model-backed. “Implicit” means intermediate information is not automatically broadcast; “explicit” means selected evidence is available to other task processes. Both must still generate inspectable experiment records. These terms imply no phenomenal consciousness, biological identity, hidden reasoning access, or permanent hierarchy.

An uncertainty estimate must identify a predicted event, such as the original proposal satisfying a frozen acceptance criterion if evaluated against the captured pre-escalation state without further repair. “Confidence” without a target is not a measurement. Record the original proposal, probability, state identifier, and timestamp before escalation or repair. Deliberation must identify the actual added computation: extra inference, another observation, a verifier, or a deterministic check. Freeze these choices before running.

## Proposed design

Use 12 held-out tasks, four each emphasizing evidence conflict, stale observations, and tool/deadline changes. All arms begin with identical available sensor/tool affordances. Selective sharing changes cross-module availability, not the environment's ground truth. Keep evaluator answer keys inaccessible to workers. Use paired task and failure schedules and two model sampling-seed identifiers. A shared seed is a reproducibility label, not a guarantee of identical provider draws.

The core factorial has two sharing conditions (local-only or selective shared evidence) and four escalation policies (always, never, adaptive, or development-frequency random): eight variants × 12 tasks × two repetitions = 192 runs. Add a simple development-tuned threshold controller with selective sharing for 24 runs, and a confidence-permuted version of the adaptive shared condition for 24 runs. Maximum: 240 runs.

Precompute the development-frequency random control's escalation counts from matched development episodes, then freeze the assignment and random positions before holdout evaluation. Counts cannot be chosen after viewing holdout outcomes. The held-out adaptive policy may use different realized counts. This comparison estimates policy utility under common caps, not a benefit at matched realized verification counts. Report realized costs and performance–cost curves. A stronger claim about the causal value of allocating a fixed amount of verification requires a separately preregistered realized-count replay or controlled allocation design with environment resets; do not obtain that claim by retrospectively conditioning the primary comparison on post-treatment costs.

Compare against development-selected simple thresholds using observed features such as missing evidence or repeated tool failure. A learned mechanism must earn its added complexity. Confidence permutation preserves the empirical distribution while breaking task-specific information; freeze which blocks permit permutation without mixing task identities or leaking labels.

## Measurements

Primary contrast: independently accepted task success for adaptive selective sharing versus development-frequency random selective sharing within the same declared caps. This is an operational policy-utility comparison; report realized verification counts and costs separately rather than assuming equal use or inventing a post hoc scalar utility. Report paired outcomes and uncertainty at the task level, averaging sampling repetitions first. The small pilot is descriptive and cannot reliably resolve small effects. Other factorial contrasts and interactions are exploratory; do not choose a successful one afterward as the primary result.

Secondary: stale or conflicting actions, verification count, evidence/communication volume, accepted results per cost, latency, and confidence quality. The default plan independently labels every original pre-escalation proposal in every episode, including proposals the actor never checks. Evaluate against the captured pre-escalation state using a hidden ground-truth evaluator or isolated replay that cannot change the actor's environment. Labels describe the original proposal, not the repaired answer or final task outcome. Later verification and repair may not retroactively replace a proposal or probability in the scoring record.

Compute the Brier score and risk–coverage curve from this complete original-proposal label set. Scoring only actor-selected checks would introduce verification selection bias. Keep offline labels and assessment work entirely outside the actor's decision path, and disclose offline evaluator cost separately from online verification, along with the combined cost. If complete labeling is infeasible, a prospective protocol amendment must specify randomized audits with known positive sampling probabilities and appropriate weighted estimates; convenience sampling of checked proposals is not a valid substitute. A calibrated score is useful only if acting on it improves the declared decision objective.

Inspect traces to distinguish better evidence selection from simply hiding difficult observations. Record information not delivered, delays, selection decisions, and effects. Explanations produced afterward cannot substitute for causal records.

## Budgets and stopping

Proposed per-run caps: 120 seconds, two CPU threads, 16 GiB host memory, 4 GiB GPU memory, 20 tools, 32,768 cumulative model input tokens, and 2,048 cumulative output tokens. All decision-path workers and online verifiers share the run cap; additional agents do not receive free budgets. Aggregate actor execution: nine elapsed hours, 7,864,320 input tokens, 491,520 output tokens, zero paid spend. Offline assessment has a separate proposed cap of one hour, two CPU threads, 4 GiB host memory, zero model calls, and zero paid spend. Report each cost ledger and their combined total; evaluator work cannot provide extra information or computation to the actor. Record acquisition, resident memory, and initialization as separate costs. Unknown energy stays unknown; tokens and prices are operational proxies.

Complete the frozen matrix or stop at a cap/validity failure. Do not stop for a favorable effect. Timeouts and task-caused tool failures remain outcomes. Preserve infrastructure-invalidated runs and repeat a complete paired block only under a documented amendment. An incomplete matrix remains an incomplete pilot.

## Freeze gate and interpretation

Fix tasks, seeds, delayed/failure schedules, model versions, hardware, shared-state semantics, escalation operation, original-proposal confidence event, pre-escalation state capture, complete labeling, development-frequency random counts, baseline thresholds, both budget ledgers, offline evaluator isolation, and analysis script before preregistration. If the labeling cap is reached before complete labels exist, report incomplete confidence assessment; do not score the selectively available subset as though it were complete. The current code may be replaced to implement these mechanisms faithfully. New questions or revisions create new protocol versions while preserving earlier evidence.

The hypothesis loses support when development-frequency random or fixed rules perform as well, costs explain the entire gain, confidence permutation changes nothing, or selective sharing increases stale actions. Any positive result concerns functional coordination on this distribution. No outcome is a consciousness test or proof of human-like thought.
