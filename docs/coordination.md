# Coordination for a research project

**Operating mode:** manual coordination with an offline consistency checker. No autonomous coordinator, GitHub Project writer, resource lease service, or remote-stop mechanism is deployed by this contract.

**Purpose:** let agents investigate and change the project rapidly while preserving what was authorized, what was attempted, what evidence applies, and what remains unresolved. The current implementation and this coordination protocol remain revisable under [ADR 0002](adr/0002-research-governs-implementation.md).

The [source review](research/github-coordination-review.md) explains the research behind these choices. [ADR 0003](adr/0003-research-coordination.md) records the decision; the [adoption record](coordination-adoption.md) records observed capabilities and the bounded integration scope.

## 1. Minimum useful operating procedure

1. Identify the question, existing authorization, task specification, protected evaluation material, mutable paths, relevant shared resources, and completion criterion. Use the [task contract](../.agents/templates/task-contract.md); a GitHub issue is optional at inception.
2. A coordinator acting within the existing controller authority admits a bounded assignment. Identify a single integrator for the accepted branch and any conflicting shared resources. Independent investigations can proceed concurrently in separate scopes.
3. Workers submit candidate artifacts and observations. Preserve attempts and relevant raw evidence. A worker's report proposes a state update; it does not grant itself authority or certify acceptance.
4. The evaluator assesses the exact submitted subject. The coordinator records the applicable review and next action in a versioned record. A completed negative or inconclusive investigation is a useful completed task.
5. Validate the complete record collection and integrate the reviewed change without overwriting a newer branch head. If a Project is bound later, project the committed record through a link and compact summary, then read the remote state back.
6. On a conflict, incomplete observation, or uncertain effect, preserve the evidence and narrow the next action. Continue independent work whose prerequisites and resources are unaffected.

This procedure adds no new approval ritual to work the owner has already authorized. Material scope expansion follows the existing owner instructions. Roles are responsibilities for a task, not a permanent cognitive hierarchy or a requirement for a central inference router.

## 2. Authority and authoritative homes

The existing [worker/evaluator/controller distinction](agent-harness.md) remains. The owner establishes goals and permissions; the coordinator performs the controller's record-serialization and integration responsibility. The evaluator controls applicable acceptance criteria; workers submit candidates. One actor may legitimately perform several responsibilities, but the candidate author cannot certify its own acceptance. Different role labels on the same author's report do not establish independently controlled review.

| Datum | Authoritative home | GitHub Project representation |
| --- | --- | --- |
| Purpose, authority, resource limits | Authenticated owner instructions plus versioned repository policy | Link; no label or comment prefix grants authority |
| Task scope and completion criterion | Versioned task contract; preserve the admitted issue-body contents when an issue is used | Task title, canonical link, short next action |
| Hypothesis and experimental design | Existing `research/HYP-*` and `experiments/EXP-*` records, with specific revisions | Links; no duplicate experiment registry |
| Candidate and evaluation evidence | Versioned subject manifest, review receipt, retained raw artifacts and digests | Evidence link and bounded interpretation |
| Accepted coordination history | Reviewed records under `harness/coordination/records/`, referenced by commit and record digest | Phase, attention, next action, record link, observation time |
| Worker progress or request | Source report with provenance; preserve exact accepted content when material | A report link until it has been reconciled |
| Architectural adoption | A distinct research decision with rationale and applicable evidence | Decision link; never inferred from issue closure or green CI |

GitHub comments are editable and deletable. A pinned comment is therefore a navigation aid. Accepted content needed to interpret research is preserved independently of that mutable object. [GitHub comment API](https://docs.github.com/en/rest/issues/comments)

Git history and content hashes do not create authentication, write-once storage, or permanent artifact availability. Preserve referenced commits and artifacts through ordinary reviewed history and appropriate backups. A changed/deleted source creates a provenance discrepancy; it does not silently rewrite the accepted content. Record retrieval failures and expiring evidence honestly.

Shared GitHub credentials cannot authenticate individual agent sessions. Actor names, reviewer IDs, URLs, role labels, and receipt strings in JSON are provenance claims until checked against a trusted source. The offline checker verifies consistency of those claims, not their truth or authorization.

## 3. Separate progress, assessment, and scientific decisions

Keep the existing phase vocabulary. Do not create or rename live Project options until their actual meanings are inventoried.

| Phase | Meaning |
| --- | --- |
| Proposed | A question or task is recorded; membership does not admit execution |
| Investigating | Bounded discovery or development is underway within existing permission |
| Authorized | Scope, prerequisites, resources, and completion method have been admitted |
| Implementing | The admitted task is being carried out; the output may be code, a review, or an experiment |
| Submitted | A concrete candidate/output and its identity are available for review |
| Evaluating | Applicable independent acceptance work is in progress |
| Accepted | The scoped deliverable and its bounded assessment were accepted |
| Rejected | The submitted deliverable failed its applicable acceptance requirements |

`Blocked` is an orthogonal condition: preserve the phase in which the task is blocked and name the unmet condition. A Project may display Blocked if that is its established vocabulary. Cancellation and supersession are dispositions, not fabricated accepted results. The precise machine-checkable transitions and record fields are specified in the [record format](../harness/coordination/examples/README.md).

An experiment's completion criterion may be a faithfully executed comparison and an honest, reproducible analysis. It need not require the proposed mechanism to win. Keep technical result, scientific result, workflow acceptance, and architectural adoption distinct. An evaluator defect can make a run invalid while an investigation documenting that defect is accepted work. Unresolved external effects can remain visible after a report is complete.

Rejection of a hypothesis, rejection of a patch, and invalidation of a measurement are different events. Do not collapse them into a red card. Do not change historical conclusions when a later architecture supersedes a candidate; record which earlier evidence remains valid and which decisions need renewed assessment.

## 4. Bind acceptance to the full subject

The record checker binds an assessment to the exact submitted identity set:

| Identity | Contents of the referenced immutable manifest/artifact |
| --- | --- |
| Task specification | Question, admitted scope, completion method, protected material, authorized envelope |
| Candidate | Code/artifact, configuration, model/checkpoint, prompt/tool configuration where relevant |
| Protocol | Exploratory/confirmatory designation, treatment arms, frozen rules, deviations/amendments |
| Evaluator | Scorer, tests/rubric, acceptance policy, independent-control boundary |
| Inputs | Dataset/split or generator, seed policy, acquisition evidence and access conditions |
| Environment | Software/hardware identities, resource limits, measured usage and unavailable measurements |
| Analysis | Analysis plan and implementation, exclusions, aggregation, uncertainty and interpretation scope |

Bind these by immutable identities, not `main`, a latest-build URL, an issue number alone, or a model marketing name. A content digest may identify a manifest that explicitly records unavailable provider internals; it does not make those internals known. Receipts need resolvable locations as well as identities when the evidence will be reviewed or reproduced.

Public coordination records contain appropriate identities and access-controlled artifact locations, not protected holdout contents. Seeds or generator settings that reconstruct hidden evaluation material remain evaluator-controlled until the protocol permits their release. Reproducibility requires an appropriate preservation and access procedure; it does not require leaking the evaluation before it is used.

Non-experimental tasks may explicitly mark unused dimensions not applicable with a reason. Do not invent a dataset, hardware result, or model experiment for a literature review or small coordination change. The task specification and actual submitted artifact still need stable identities.

Changing the task specification, candidate, evaluator, inputs, environment, protocol, or analysis makes old acceptance inapplicable to the changed subject unless a new assessment explicitly establishes applicability. Preserve the old result. Check the integrated candidate when changes can interact; a clean text merge and separately passing branches do not establish integrated correctness.

The structure borrows provenance distinctions among entities, activities, plans, revisions, and responsibility from [W3C PROV-DM](https://www.w3.org/TR/prov-dm/). It does not require the full PROV interchange format.

## 5. Versioned records and logical operations

Records use explicit schema versions, stable task and operation identifiers, per-task revisions, and previous-record digests. Validate the complete relevant collection; selecting whichever comment has the newest timestamp is not conflict resolution. Source report time and coordinator observation time are recorded separately in UTC. They are not used to infer process liveness, synchronized clocks, or exclusive ownership.

An identical replay of an operation has one logical effect. Reusing an operation ID with a different immutable payload is a conflict. Two different records extending the same task revision are a conflict. A missing predecessor is incomplete history. Preserve the conflicting reports for reconciliation; do not choose a winner by timestamp.

The offline checker detects conflicts in the records supplied to it. It does not serialize competing writers on a server. In manual operation one named integrator accepts the next record into the reviewed branch. Use the Git endpoint's actual non-force conflict behavior or a documented lease check, read the head after rejection, and re-plan. Do not turn a client-side comparison into an undocumented server-side guarantee.

Schema evolution is an explicit change. Preserve old records, state the version migration and compatibility rules, exercise old examples, and version the checker alongside them. Unsupported versions stop the affected interpretation; they do not invite silently dropping unfamiliar authority or control data. Future checkpoint/pruning support must preserve predecessor proofs and declared collection boundaries before histories are compacted.

## 6. Dependencies and changing evidence

Only execution prerequisites block admission. Conceptual links such as related-to, derived-from, and future research questions can form a rich cyclic research graph.

Execution dependencies identify specific accepted artifact/record revisions, not just task names or closed issues. Distinguish unmet planning requirements from satisfied pinned prerequisites. Unmet requirements stay in the task specification and blockers; they must be resolved before the affected execution begins.

Validate dependency edges at the revision level. A later A iteration can use an earlier B result while a later B iteration uses an earlier A result; collapsing both to task names would invent a cycle. A real circular prerequisite or missing pinned record prevents the dependent admission.

Discovery of leaked evaluation data or another invalid premise triggers a search for dependent decisions and a recorded reassessment. It does not erase history or automatically prove every descendant false. The coordinator/evaluator must decide whether the affected premise was necessary. The current checker does not discover semantic dependencies omitted from the records.

## 7. Shared resources, holds, and resumption

An issue ID is not a resource lock. Assignments should identify overlapping writable paths, shared branch/ref, generated outputs, evaluator material, databases, external targets, and exclusive benchmark devices as relevant. Two disjoint source edits can also conflict semantically through a shared contract.

Current reservations are cooperative and manually reconciled. Separate worktrees do not isolate hardware contention, credentials, external services, or shared databases. The coordinator serializes accepted integration and conflicting exclusive use; independent nonconflicting work can continue.

Keep these observations separate:

- Hold requested: no new conflicting admission in that scope.
- Stop requested: a request was sent to the running worker.
- Stop acknowledged: the worker reported receiving it.
- Stop confirmed: an appropriate executor/observer established that execution stopped.
- Effects unresolved or reconciled: earlier external operations remain uncertain or have been accounted for.

A process can be stopped before acknowledging a request. It can also stop after sending an external operation whose outcome remains unknown. Conflicting replacement work waits for effect reconciliation or actual resource-side fencing. Clearing an uncertainty flag requires a recorded resolution; the checker can require that reference but cannot certify the external fact.

An expired observation or a newer worker comment does not authorize takeover. A future automated resource controller needs grants whose stale generations are rejected at the affected resource. Chubby's recipient-validated sequencers illustrate that enforcement property; a Project field or local timestamp does not implement it. [Burrows, OSDI 2006](https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows_html/index.html)

## 8. GitHub projection and recovery contract

The [capability review](research/github-coordination-review.md) records current documented APIs. The live Project's owner, IDs, fields, options, views, workflows, permissions, and UI remain unbound until inspected. Repository push access does not establish Project access.

For a future adapter, preserve a durable intent before any write: operation ID, canonical record revision/hash, target identity, expected preimage, intended postimage, dependencies, attempt number, and response/readback evidence. Canonical commitment and projection confirmation are separate states.

Use `read → plan → apply → read back → reconcile` with complete pagination and validation of relevant partial errors. A timeout is `outcome_unknown`. One empty read cannot prove that an earlier request will not arrive later. Comment projection may create physical duplicates; reconcile one logical operation by its stable ID and unchanged payload, preserving discrepancy evidence. This is not an exactly-once API contract. [AWS Builders' Library](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

For mutable fields, detect intervening human/workflow changes and re-plan. A rollback is another write subject to drift. Show mixed projection state rather than a global success marker when only some targets match. Record which canonical revision each remote target currently represents.

Preserve field/option identity across display-name changes. Distinguish unrequested, missing, null, inaccessible, and deleted values. A permission failure must not drive deletion. Bound retries and API cost, honor rate-limit responses, and retain unknown outcomes across restart. Webhooks can prompt reconciliation; a webhook's arrival does not itself authorize a transition.

Before deployment, exercise transport failures, late/duplicate delivery, pagination gaps, permission loss, comment edits/deletion, human drift, partial field updates, and crash recovery against a fake transport. The offline record tests do not exercise these network behaviors. Production ownership, secrets, monitoring, recovery, and a disable path belong to the deployed adapter's separate contract.

## 9. Human surface and admission vocabulary

Begin with a small projection: established Status/phase, attention reason, short next action, accepted-record link, and clearly labeled observation time. Keep provenance, detailed scope, evidence, and conclusions in the linked record. Native issue/PR relationships supply navigation; a new custom field needs a demonstrated scanning or decision purpose.

Start with two or three views only if the populated workload benefits: current admitted investigations, items requiring attention/review, and an evidence/history table. The exploratory backlog remains visibly unadmitted. Completed negative and inconclusive work remains discoverable. The project has no release or alpha plan; release-oriented filters from a generic playbook are not imported.

Map built-in close/merge/status workflows explicitly before changing them. Membership capture can remain useful, but membership, readiness, ownership, evidence acceptance, and adoption remain separate. Modify only inventoried, authorized workflows and read the exact changed settings back.

Validate populated cards and drilldown at the operator's actual desktop and phone widths. Put phase, attention, and next action first; long instructions belong in one linked detail view. A browser viewport test establishes layout in that viewport only. No live Project UI or physical-device behavior is claimed by the Markdown renderer.

## 10. How this protocol earns more automation

First exercise a bounded real task through admission, candidate review, accepted negative/inconclusive analysis where appropriate, and a prospective amendment. Measure operator effort, time from report to accepted record, time from acceptance to projection, conflicting updates, incorrect admissions, unresolved effects, and evidence applicability failures. Report denominators and incomplete observations.

Add a component when a measured recurring failure or operating cost justifies it. A deterministic projection adapter, durable inbox/outbox, or enforced resource controller solves a different problem and needs its own acceptance evidence. This coordination design remains an experimental instrument; passing its tests does not establish improved agent performance or intelligence.
