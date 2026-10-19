# Offline coordination model and synthetic examples

**Demonstrations only.** No file here assigns current work, grants authority, records a real experiment, or reports scientific evidence. The invented outcome in `completed-negative.json` exercises the distinction between an accepted research deliverable and a favorable hypothesis result. Its digests are fixture values, not references to measured artifacts.

The standard-library Python checker reads records and reports consistency. It performs no network operation and does not modify supplied records. It is an executable model for the cooperative manual baseline, not an autonomous coordinator or enforcement boundary.

From the repository root:

```sh
python3 scripts/check_coordination.py
python3 scripts/check_coordination.py --examples
python3 -m unittest discover -s tests -p test_coordination.py -v
python3 scripts/check_coordination.py path/to/collection.json path/to/more-records/
```

With no arguments, the checker recursively discovers operational JSON records under `harness/coordination/records/`. When none exist, it explicitly reports **no operational validation performed**. `--examples` separately checks this synthetic directory; an explicit example path works as well. Operational discovery rejects demonstration envelopes, and demonstration and operational records are never mixed.

All supplied JSON files form **one complete collection** for the purpose of the checks. Directory arguments recursively include `*.json` descendants. Histories and referenced prerequisites must be present across the supplied files; a file need not be self-contained individually. The checker cannot establish that the caller supplied every record that actually exists outside the discovered or explicit paths.

Input is bounded to 64 files, 8 MiB total bytes, and 1,000 received records, including physical duplicates. Duplicate JSON object keys and unknown fields are errors. Exit 0 means the supplied collection satisfies the described model; exit 1 reports a failed check. The summary is sorted by task ID and is independent of transport order.

## Schema version 1

Each file is an envelope with exactly these required fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer `1`; later schemas require explicit support. |
| `demonstration` | Boolean. Demonstrations and actual records cannot be mixed in one check. |
| `records` | Immutable record payloads. Empty files are permitted within a nonempty collection. |
| `description` | Optional description of the collection. |

Every record has the following fields; `note` is the only optional record field:

| Field | Shape and rule |
| --- | --- |
| `task_id` | Stable identifier, 3–128 ASCII letters/digits or `._:-`, starting with a letter. Demonstrations start `DEMO-`. |
| `task_kind` | `investigation`, `experiment`, `implementation`, or `coordination`; constant within a task history. |
| `task_spec` | Immutable identity of the admitted task definition. A mutable issue URL alone is insufficient. |
| `operation_id` | Stable identifier with the same syntax as `task_id`; unique for each logical update across the collection. |
| `task_revision` | Positive integer; complete histories begin at 1 and increment by 1. |
| `previous_record_sha256` | Null at revision 1; otherwise the preceding record's canonical SHA-256 hex digest. |
| `source_reported_at` | ISO UTC timestamp ending in `Z`, with optional 1–6 fractional-second digits. |
| `observed_at` | Separate coordinator observation timestamp in the same format. Clock order is not asserted. |
| `phase` | One of the existing phases in the transition table below. |
| `disposition` | `active`, `completed`, `cancelled`, or `superseded`. Withdrawal/replacement needs no fabricated experiment result. |
| `binding` | Null while no submitted artifact exists; otherwise the complete seven-dimension object below. |
| `assessment` | Null or the scoped review object below. |
| `blockers` | List of unresolved next-action conditions, including planning prerequisites without accepted artifacts yet. |
| `control` | Separate hold/stop/effect facts, described below. |
| `dependencies` | List of **satisfied, pinned execution prerequisites**: `{task_id, task_revision, record_sha256}`. |
| `related` | List of conceptual references; no execution semantics, existence requirement, or cycle restriction. |
| `note` | Optional nonempty text for limitations, decisions, or a demonstration label. |

An immutable identity is `sha256:<64 lowercase hex characters>` or `git:<40 or 64 lowercase hex characters>`. These identify content by convention. The checker validates identity shape and exact correspondence, and **does not retrieve or hash the referenced artifact**.

### Binding and assessment

`binding` contains exactly `task_spec`, `candidate`, `protocol`, `evaluator`, `inputs`, `environment`, and `analysis`. The `task_spec` identity must equal the record's admitted definition. `candidate` identifies the submitted code, document, configuration, or other scoped artifact.

For `experiment` tasks, all seven dimensions require immutable identities. Referenced input and environment manifests should identify datasets/generators/splits, seeds, model/tool versions, hardware, resource limits and accounting, and known reproducibility limits. The protocol/analysis references should identify exploratory or confirmatory mode and the applicable plan. Those contents and their scientific adequacy remain review responsibilities; this checker does not dereference them.

For other task kinds, `task_spec` and `candidate` still require immutable identities. Any unused remaining dimension may be an explicit `not_applicable:<nonempty reason>` string. A literature review therefore need not invent a compute environment or dataset. The complete strings, including their reasons, participate in exact binding comparisons.

An `assessment` contains exactly:

```text
binding: exact copy of the assessed binding
acceptance: passed | failed | not_assessed
technical_result: pass | fail | not_assessed | not_applicable
scientific_result: supports | weakens | inconclusive | invalid_experiment | not_assessed | not_applicable
reviewer: nonempty metadata string
receipt: nonempty reference string
```

`acceptance` concerns the bounded deliverable. `Accepted` requires `acceptance: passed`, a full binding, no unresolved deliverable blockers, and a terminal disposition. It does not require `scientific_result: supports` or `technical_result: pass`. A reviewed report documenting a failed/invalid attempt can be an accepted deliverable. `Rejected` requires a full binding, `acceptance: failed`, and a terminal disposition; it means the submitted deliverable failed acceptance. Early withdrawal uses cancellation or supersession without inventing an assessment. Scientific adoption is a separate decision, outside this record's acceptance field.

Assessments are allowed only in `Evaluating`, `Accepted`, and `Rejected`. A changed binding must first be recorded without an assessment and cannot remain `Accepted`; later review needs an exact new binding. One receipt reference cannot be relabeled for another binding. If one real report contains several assessments, use distinct section/record references for their scoped receipts.

Reviewer names, receipt links, and role claims are metadata. A fabricated but structurally valid name can pass this checker. Independent review and authenticated owner instructions must be established through the actual operating workflow.

### Phase transitions

Every history starts `Proposed` at revision 1. Same-phase observations are permitted. These are the additional permitted successors:

| Current phase | Permitted next phase |
| --- | --- |
| Proposed | Investigating, Authorized |
| Investigating | Authorized, Submitted (non-experiment tasks only) |
| Authorized | Implementing, Investigating |
| Implementing | Submitted, Investigating |
| Submitted | Evaluating, Rejected, Investigating |
| Evaluating | Accepted, Rejected, Implementing, Investigating |
| Accepted | Investigating |
| Rejected | Investigating |

A full artifact binding is required in `Submitted`, `Evaluating`, `Accepted`, and `Rejected`. Earlier phases can use null while retaining the pinned task definition. `Investigating → Submitted` supports non-experimental literature/analysis deliverables within already authorized scope; it does not grant permission for external actions or paid runs. New experiment records must pass through `Authorized → Implementing → Submitted`. A review of pre-existing evidence can be an `investigation` task rather than pretending to execute an experiment.

Entering or reactivating `Authorized`/`Implementing` requires active disposition and no unresolved blockers, hold, stop request, or unresolved effects. A new blocker or hold can be reported without pretending the currently recorded process phase instantly changed. Completed disposition requires `Accepted` or `Rejected`; cancellation and supersession can record withdrawal at any phase without fabricating a scientific assessment. An accepted task can return to investigation with a prospective revision. Changing the task definition requires investigation and a fresh assessment; a new experiment then needs fresh admission. Experiment bindings can change during investigation, admitted implementation, or its submission, and cannot be replaced in a same-phase submission to bypass that path. History remains intact.

### Hold, stop, and unresolved effects

`control` contains five independent Boolean fields plus a nullable metadata reference:

```text
hold_requested
stop_requested
stop_acknowledged
stop_confirmed
unresolved_effects
resolution_receipt
```

A hold prevents new admission but says nothing about process liveness. Stop acknowledgement requires a recorded stop request. Executor-confirmed stop does **not** require worker acknowledgement: a process may be stopped before it acknowledges anything. Neither proves that already-sent external writes have settled.

Clearing unresolved effects or releasing a hold requires a nonempty `resolution_receipt`. Clearing a stop request for resumption requires the preceding record to report confirmed stop and resolved effects, plus a resolution receipt. These are declarations with provenance fields, not mechanically verified resource facts. A fake receipt cannot make a real resource safe.

Unresolved external effects can persist after an accepted research failure report. They remain visible as attention and block later modeled execution entry. Cross-worker resource handoff, cross-issue overlap, stale process rejection, and actual external-effect reconciliation are not implemented by this checker.

### History, duplicates, and prerequisites

The canonical record digest is SHA-256 over UTF-8 encoding of Python's `json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)`. It covers every record field, including notes and receipt metadata. It is independent of source JSON formatting. This local canonicalization is not a signature or a claim of general JSON canonicalization-standard support.

An identical repeated operation is counted once even if it appears in two files or comments. Reuse of its ID with a changed immutable payload fails. Two different operations claiming one task revision fail. Revision gaps, changed earlier content, and previous-hash mismatch fail. No timestamp selects a winner among competing records; hashes do not establish the writer's authority or make storage immutable.

`dependencies` contains already accepted deliverable records with exact task/revision/digest pins. It does not mean that the prerequisite's hypothesis succeeded. Unknown future prerequisites belong in the task specification and `blockers`, so a proposed task remains representable before upstream work is accepted.

The checker detects missing pins, mismatched digests, unaccepted prerequisite deliverables, and cycles across versioned execution dependencies plus revision ancestry. A@2 depending on B@1 and B@2 depending on A@1 can be a valid research iteration. Collapsing those nodes into task IDs would create a misleading apparent cycle. `related` references carry no admission semantics.

The checker cannot discover subsequently invalidated evidence that was omitted from its input, nor decide whether an old valid artifact applies to a new question. Reassessment of upstream evidence and affected downstream decisions remains an explicit review responsibility.

## What a successful check establishes

It establishes internal consistency of the supplied history, phase transitions, declared control facts, exact assessment bindings, duplicate handling, and pinned prerequisite graph under schema 1. The tests exercise concrete failure traces and explicitly demonstrate that plausible reviewer metadata is not authenticated.

It does not establish record completeness, real actor identity, authorization, process liveness, actual resource ownership, artifact availability/content, statistical validity, absence of leakage, raw-run execution, or GitHub/API synchronization. There is no network writer, daemon, lease, scheduler, stop mechanism, or real task record here. Live concurrency, resource fencing, webhook/API recovery, and production handoff behavior need separate conformance tests if those capabilities are later built.
