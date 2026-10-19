# Research appraisal: GitHub coordination for evolving experiments

**Reviewed:** 2026-10-19. **Scope:** the supplied `github-project-agent-coordination.md`, repository source at `92a73ad56f9f169c956ea202455d3a627238e53d`, live repository metadata, and current primary documentation. No live Project API/UI, deployed worker controller, or model-performance experiment was exercised for this appraisal.

## Main finding

The supplied playbook has a useful separation: protocol, GitHub projection, and operator interface. The adaptation should strengthen evidence identity and recovery while preserving a small manual baseline. A Project is useful for coordinating investigations, but it cannot establish the truth of a hypothesis, the authenticity of a role label, or the termination of a remote effect.

The largest project-specific change is the meaning of completion. A valid negative result may complete a scientific task. An invalid measurement, rejected patch, cancelled investigation, and superseded design each mean something different. The [coordination contract](../coordination.md) keeps those distinctions explicit.

## Evidence register

| Source | Verified documented fact | Design consequence or limit |
| --- | --- | --- |
| [GitHub REST Project fields][G1], [items][G2], [views][G3] | Current Projects v2 REST includes field/item operations and view creation. Item PATCH accepts multiple field values; views expose layout/filter/visibility/grouping/sorting inputs. | Do not assume GraphQL-only access or transactional batch behavior. Owner type and endpoint matter. |
| [Projects in Actions][G4] | The repository `GITHUB_TOKEN` cannot access Projects. User/organization workflows require an appropriate distinct credential capability. | Repository push permission does not prove Project access. No credentials are created by this work. |
| [User-owned view endpoint][G3] | The documented endpoint rejects App user/installation tokens and fine-grained PATs. | Verify the exact operation and owner type; do not generalize organization support to a personal Project. |
| [GraphQL Projects schema][G5] | Existing single-select option IDs can be preserved during updates; the documentation warns about item-value loss when IDs are omitted. | Names are display properties, not stable identities. Do not delete/recreate options as a rename strategy. |
| [Issue-comment API][G6] | Comments can be edited, deleted, and pinned. | Preserve accepted content independently. Pinning and append-only convention are not immutability. |
| [REST best practices][G7] | Conditional unsafe-method requests are unsupported unless the individual endpoint says otherwise. | A read/preimage check leaves a race; no assumed compare-and-swap over comments or fields. |
| [Webhook troubleshooting][G8], [failed delivery][G9], [best practices][G10] | Delivery can be delayed or out of order; failures are not automatically redelivered; requested redelivery retains its delivery GUID. | Delivery identity, logical-operation identity, accepted revision, and complete reconciliation remain separate. |
| [GraphQL limits][G11], [pagination][G12] | Errors can accompany HTTP 200/partial results; connection traversal is explicit. | Reject authoritative interpretation of relevant partial data and traverse every required connection. |
| [Actions concurrency][G13] | Default behavior replaces the previous pending run. Optional `queue: max` permits up to 100 waiting runs; ordering is by entry into the wait, with overflow cancellation. | Neither mode is an unlimited event log or exclusion mechanism for external agents/resources. |
| [Built-in Project automations][G14] | GitHub documents lifecycle-driven status writers and UI workflow controls. | Inventory actual enabled workflows before deciding whether they conflict with acceptance. Defaults are not observed live settings. |
| [AWS idempotent API design][S1] | Robust retry contracts account for caller request identity, changed parameters, delayed requests, and retained deduplication state. | A GitHub comment marker supplies correlation, not a server-side exactly-once contract. |
| [Chubby][S2] | A protected recipient validates a sequencer and rejects stale generations; the paper also discusses imperfect delay-based protection. | A lease or timestamp is insufficient without enforcement at the affected resource. |
| [W3C PROV-DM][S3] | Provenance distinguishes entities, activities, plans, derivation, revision, and responsibility. | Record what changed and what a result depends on without adopting an entire ontology as the architecture. |

### Documentation and capability gaps

The REST field-creation parameter table and examples currently present inconsistent requirements across field types. The GraphQL view configuration input does not expose every REST view-creation control in the same shape. A public Project-workflow enable/disable mutation was not located in this review; Actions workflow controls concern a different resource. These are reasons for capability-specific probes and adapters, not invented endpoints. [G1], [G3], [G5], [G14]

The available connection exposed repository operations but no callable Projects operation during this task. No Project URL/number was supplied. Owner type, actual views/options/workflows, Project permission, native-app behavior, and worker topology remain unknown. Repository metadata saying Projects is enabled does not establish that a Project exists, is linked, is visible, or is writable.

## Engineering deductions

### Preserve a research subject, not just a commit

A matching source commit can still have a different scorer, dataset, prompt, model route, analysis, or resource limit. Acceptance should bind the exact relevant identity set. A changed architecture can make earlier evidence inapplicable to a new claim without making the old observation false. An evaluator defect can instead undermine the validity of a past inference. These require different records and reassessment.

### Make uncertainty durable

After a timed-out append, an empty read does not prove the initial request cannot arrive later. A retry and the original can both appear. Accept one logical operation for the same ID/payload; preserve physical duplicate projections and reconcile. The same ID with a changed payload is a conflict. This is a design deduction; the current offline checker does not exercise a GitHub transport.

Likewise, worker exit does not settle already-sent writes. A completed investigation can document a failed/invalid attempt while affected resource reuse remains blocked. Acknowledgement, stop confirmation, and resolution of external effects should never be one boolean.

### Use versioned prerequisites

Only execution prerequisites should block work. Keep conceptual research links unrestricted. Pin a fulfilled prerequisite to its accepted record revision; keep unresolved requirements explicit. Detect cycles at the revision level so iterative A/B research is not rejected merely because task names recur. Upstream invalidation initiates reassessment of affected decisions, not automatic deletion or universal rejection of descendants.

### Choose a small enforceable subset

The initial record checker is deliberately local and read-only. It can detect incompatible records supplied together, compare acceptance identities, and expose recorded blockers. It cannot observe all real actors, authenticate their claims, stop a process, fetch hidden evidence, or serialize a GitHub server. A manual coordinator remains responsible for the unimplemented boundaries.

## Concrete repository defect

At the inspected base revision, `scripts/check_research.py` asserted that EXP-0001 remained planned with null results, ignored EXP-0002 through EXP-0004, and permanently required a particular Rust source file. This was observed directly in source. Those checks accidentally encoded an inception snapshot as the future validity condition.

The replacement discovers experiment manifests and checks a documented common structure and lifecycle/result shape. It permits completed exploratory, negative, and inconclusive results. Structural success is not evidence validation, authorization, or scientific confirmation. The [record guide](../../harness/coordination/README.md) describes the minimum result object.

## Failure cases and verification boundaries

| Case | Required response | Layer exercised or still required |
| --- | --- | --- |
| Negative/inconclusive comparison with accepted analysis | Permit completed research without adoption | Offline record/manifest checks |
| Same operation replayed unchanged | One logical record | Offline record checks |
| Same operation ID with changed payload | Conflict | Offline record checks |
| Competing successor revisions or missing history | Conflict/incomplete collection, no timestamp winner | Offline record checks |
| Candidate/specification/scorer/data/analysis changes | Old acceptance does not match the changed subject | Offline binding checks |
| Missing or circular pinned prerequisite | Prevent affected admission/interpretation | Offline dependency checks |
| Hold acknowledgement while effects remain uncertain | Preserve separate control facts | Offline consistency checks; real effect observation remains manual |
| Comment arrives after a timeout and retry | Reconcile logical identity; tolerate physical duplicates | Future fake-transport and live adapter checks |
| Field write succeeds but record-link write fails | Preserve canonical revision; show partial projection | Future adapter checks |
| Old source comment edited/deleted | Compare retained accepted contents, surface discrepancy | Manual review/future adapter |
| Pagination truncates or permission is lost | Incomplete observation, no destructive inference | Future adapter checks |
| Two issues compete for the same GPU, branch, or scorer | Resolve resource conflict across issue IDs | Manual scope review/future resource controller |
| Worker stops with an external request pending | Reconcile or fence effects before conflicting replacement | Manual observation/future executor and resource tests |
| Upstream evaluator defect affects a prior decision | Preserve history and assess dependent claims | Scientific review; no automatic semantic invalidation |

The test suite exercises a bounded consistency model. These tests are neither formal verification of a distributed system nor measurements of coordination effectiveness. The smallest next operational study is one admitted task and amendment with recorded operator cost, staleness, conflicts, and evidence-applicability failures, as specified in the [contract](../coordination.md).

## Primary sources

The evidence register links the primary documents used in this review. API capabilities are documented observations as of the review date; a live adapter still needs to establish its actual owner-specific access and endpoint behavior.

[G1]: https://docs.github.com/en/rest/projects/fields
[G2]: https://docs.github.com/en/rest/projects/items
[G3]: https://docs.github.com/en/rest/projects/views
[G4]: https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/automating-projects-using-actions
[G5]: https://docs.github.com/en/graphql/reference/projects
[G6]: https://docs.github.com/en/rest/issues/comments
[G7]: https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api
[G8]: https://docs.github.com/en/webhooks/testing-and-troubleshooting-webhooks/troubleshooting-webhooks
[G9]: https://docs.github.com/en/webhooks/using-webhooks/handling-failed-webhook-deliveries
[G10]: https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks
[G11]: https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api
[G12]: https://docs.github.com/en/graphql/guides/using-pagination-in-the-graphql-api
[G13]: https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency
[G14]: https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations
[S1]: https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
[S2]: https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows_html/index.html
[S3]: https://www.w3.org/TR/prov-dm/
