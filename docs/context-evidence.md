# Recoverable context and evidence contract

**Status:** proposed mechanism and acceptance criteria; not implemented. Motivated partly by the [HELIX source review](research/helix-context-review.md), with benefits to be tested in [EXP-0005](../experiments/EXP-0005/protocol.md).

## The distinction that governs this design

Information retained somewhere is not necessarily information the agent can find, understand, or use. Preserve three separate properties:

1. Byte recovery: an authorized reader can retrieve the retained original.
2. Evidence discovery: the task interface makes relevant omitted evidence discoverable.
3. Decision preservation: the agent still makes acceptable decisions under the projected context.

The first can be tested mechanically. It does not establish the other two. A summary, receipt, vector, or hash is not a lossless replacement for arbitrary questions about its source.

## Observation to receipt

Persist an authorized observation before retiring its eligible model-visible contents. Verify its identity and retrieval path. An illustrative receipt contains:

```text
receipt_id; task_id; task_revision; operation_id
source_identity; source_revision; observed_at; environment_identity
artifact_location; digest; byte_count; retention_state; access_scope
operation_status; exit_code_if_known; settlement_state
projection_kind; projection_version; coverage; explicit_omissions
scoped_check_results; checker_identity; input_bindings
retrieval_interface; range_or_section_hints; retrieval_availability
validity_conditions; invalidation_dependencies
```

These are proposed semantic fields, not a frozen wire schema. A digest identifies bytes, not source authenticity, truth, safety, or permission. A location is needed in addition to a digest. Retrieval is scoped and read-only; an evidence handle is never executable code.

Filter already retained output, not a new invocation of its original command. A repeated command can observe a different state or repeat an irreversible effect. Preserve that difference explicitly when fresh observation is actually intended.

## Privacy and retention

Archive only data within the task's authorization. Do not collect credentials or private model reasoning. Sensitive artifacts need access control and a declared retention policy. Public reports use safe projections rather than private logs or hidden evaluation inputs.

If authorized redaction occurs before retention, identify the retained version as redacted; do not advertise recovery of bytes never kept. Expired, deleted, corrupt, denied, or missing artifacts have typed unavailable states. Do not conceal them behind an apparently valid handle. Recover or retain sufficient inline evidence when allowed; otherwise block the dependent claim or operation. Safety checks remain fail-closed.

## Projection eligibility

Only completed and sufficiently settled historical work is eligible under a versioned policy. Preserve or explicitly re-establish:

- Current goals, constraints, authorization, task revision, and resource limits.
- Active failure evidence, unresolved contradictions, uncertain effects, and reasons a live hypothesis may be wrong.
- Recent work needed for the next decision and call/result relationships required by the native protocol.
- Exact evidence required by the pending evaluator or an explicit request.

Age and byte length alone do not establish irrelevance. Goal changes can make old evidence relevant again. Eligibility checks must be reevaluated after content, dependencies, permissions, or task revisions change. Never rewrite privileged instructions as ordinary retrieved memory.

Start with deterministic typed summaries for supported observations and a conservative unmodified fallback for unsupported content. Do not use an LLM summarizer as an uncounted background worker. A learned compressor is a separate treatment with its own cost and quality evaluation.

## Progressive retrieval

A bounded index exposes source identity, observation type, scope, coverage, and useful retrieval hints. Readers can expand a receipt, retrieve an exact range, or request the full authorized artifact. Include counterevidence, not only matching supportive material.

Measure failed searches, unavailable handles, retrieval calls, time to find decisive evidence, and decisions after retrieval. Avoid testing only exact lookup by a handle already supplied to the agent: that bypasses the discovery problem.

## Compatible deltas

A test delta requires complete, compatible reports with stable test identities, selection, runner, and environment; it names both source revisions. Counts alone cannot identify resolved tests. Incompatible, incomplete, or zero-test results do not imply success.

Represent resolved, introduced, remaining, skipped, and changed outcomes separately. Preserve traceback recovery. A delta reports observed behavior; independent acceptance still evaluates the exact candidate under its rubric.

## Cache-aware, not token-only

Keep static instructions and tool definitions stable where compatible with current authority. Prefer explicit task-specific changes over unnecessary prefix churn. A batch-retirement policy is an experimental option, not a hard-coded optimization.

Do not preserve a false or stale statement merely to keep a cache hit. Do not assume shorter payloads are cheaper: cache reads/writes, extra retrieval, output, and request count can change the economics. Cache behavior is provider/model/version-specific. Record the actual exposed categories and rate/version when estimating price; subscription quota is a separate observation.

OpenAI's [prompt-caching documentation](https://platform.openai.com/docs/guides/prompt-caching), checked 2026-10-20, documents model-dependent caching and the importance of stable conversation/tool content. API behavior is not a promise about Codex subscription limits. HELIX's cache-stable-aging code motivates a candidate; its byte savings are not provider-token measurements.

## Supported integration only

First apply receipts to controller-owned tools and context packets. Explicitly declare which native tools and histories remain outside that control. A supported hook or tool interface may not permit arbitrary transcript replacement. Do not intercept authentication, invent proxy support, disable native compaction, or mutate opaque provider items to force the experiment to work.

## Minimum offline tests

Verify retention-before-projection; exact authorized range recovery; cold restart; corruption; access revocation; unavailable originals; instruction-bearing archived text; goal and dependency changes; duplicate/out-of-order events; active-error protection; compatible and incompatible deltas; no-tests reports; side-effect-free retrieval; unknown usage; and no repeated external operation after replay.

Then test discovery and decision quality with ambiguous or misleading receipts, rare decisive exceptions, changed goals, similar but inapplicable earlier tasks, and budget-limited retrieval. Passing byte-recovery tests is not a substitute for these agent-level comparisons.
