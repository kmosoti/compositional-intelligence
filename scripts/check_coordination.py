#!/usr/bin/env python3
"""Check supplied coordination records; never execute work or contact GitHub.

This is a bounded consistency model, not authentication, resource fencing,
scientific verification, or a guarantee that the collection is complete.
"""

import argparse
from collections import defaultdict, deque
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

PHASES = {
    "Proposed": {"Investigating", "Authorized"},
    "Investigating": {"Authorized", "Submitted"},
    "Authorized": {"Implementing", "Investigating"},
    "Implementing": {"Submitted", "Investigating"},
    "Submitted": {"Evaluating", "Rejected", "Investigating"},
    "Evaluating": {"Accepted", "Rejected", "Implementing", "Investigating"},
    "Accepted": {"Investigating"},
    "Rejected": {"Investigating"},
}
KINDS = {"investigation", "experiment", "implementation", "coordination"}
BINDING_KEYS = {"task_spec", "candidate", "protocol", "evaluator", "inputs", "environment", "analysis"}
CONTROL_FLAGS = {"hold_requested", "stop_requested", "stop_acknowledged", "stop_confirmed", "unresolved_effects"}
RECORD_KEYS = {
    "task_id", "task_kind", "task_spec", "operation_id", "task_revision",
    "previous_record_sha256", "source_reported_at", "observed_at", "phase",
    "binding", "assessment", "blockers", "control", "dependencies", "related", "disposition",
}
ID = re.compile(r"[A-Za-z][A-Za-z0-9._:-]{2,127}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
IMMUTABLE = re.compile(r"(?:sha256:[0-9a-f]{64}|git:(?:[0-9a-f]{40}|[0-9a-f]{64}))\Z")
UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z\Z")
MAX_FILES = 64
MAX_BYTES = 8 * 1024 * 1024
MAX_RECORDS = 1000


class Invalid(ValueError):
    """A structural or consistency failure in the supplied collection."""


def require(condition, message):
    if not condition:
        raise Invalid(message)


def text(value):
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 2048


def matches(pattern, value):
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def fields(value, required, where, optional=()):
    require(isinstance(value, dict), f"{where}: expected object")
    require(required <= value.keys(), f"{where}: missing fields {sorted(required - value.keys())}")
    require(value.keys() <= required | set(optional), f"{where}: unknown fields {sorted(value.keys() - required - set(optional))}")


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")


def record_hash(record):
    """Content correspondence only: no signature or author verification."""
    return hashlib.sha256(canonical(record)).hexdigest()


def check_binding(binding, record, where):
    fields(binding, BINDING_KEYS, where)
    require(binding["task_spec"] == record["task_spec"], f"{where}: task_spec differs from admitted definition")
    for key, value in binding.items():
        allowed = matches(IMMUTABLE, value)
        if record["task_kind"] != "experiment" and key not in {"task_spec", "candidate"}:
            allowed = allowed or (text(value) and value.startswith("not_applicable:") and bool(value[15:].strip()))
        require(allowed, f"{where}.{key}: expected immutable ID or permitted reasoned not_applicable entry")


def check_record(record, demonstration):
    fields(record, RECORD_KEYS, "record", {"note"})
    for key in ("task_id", "operation_id"):
        require(matches(ID, record[key]), f"record: invalid {key}")
    name = f"{record['task_id']}@{record['task_revision']}"
    require(isinstance(record["task_kind"], str) and record["task_kind"] in KINDS, f"{name}: unsupported task_kind")
    require(matches(IMMUTABLE, record["task_spec"]), f"{name}: task_spec needs an immutable ID")
    require(type(record["task_revision"]) is int and record["task_revision"] > 0, f"{name}: revision must be a positive integer")
    previous = record["previous_record_sha256"]
    require(previous is None or matches(DIGEST, previous), f"{name}: invalid previous-record digest")
    require(isinstance(record["phase"], str) and record["phase"] in PHASES, f"{name}: unsupported phase")
    require(isinstance(record["disposition"], str) and record["disposition"] in {"active", "completed", "cancelled", "superseded"}, f"{name}: unsupported disposition")
    if record["disposition"] == "completed":
        require(record["phase"] in {"Accepted", "Rejected"}, f"{name}: completed disposition requires a review decision")
    if demonstration:
        require(record["task_id"].startswith("DEMO-"), f"{name}: demonstration task IDs must start DEMO-")
    else:
        require(not record["task_id"].startswith("DEMO-"), f"{name}: operational records cannot use demonstration task IDs")
    if "note" in record:
        require(text(record["note"]), f"{name}: note must be nonempty text")
    for key in ("source_reported_at", "observed_at"):
        require(matches(UTC, record[key]), f"{name}: {key} must be ISO UTC ending in Z")
        try:
            datetime.fromisoformat(record[key].replace("Z", "+00:00"))
        except ValueError as error:
            raise Invalid(f"{name}: invalid {key}") from error
    # Clocks may disagree. Neither timestamp establishes event order or liveness.
    for key in ("blockers", "related"):
        require(isinstance(record[key], list) and all(text(item) for item in record[key]), f"{name}: {key} must be a list of nonempty strings")
    control = record["control"]
    fields(control, CONTROL_FLAGS | {"resolution_receipt"}, f"{name}.control")
    require(all(type(control[key]) is bool for key in CONTROL_FLAGS), f"{name}: control flags must be booleans")
    require(control["resolution_receipt"] is None or text(control["resolution_receipt"]), f"{name}: invalid resolution receipt")
    require(not control["stop_acknowledged"] or control["stop_requested"], f"{name}: stop acknowledgement has no request")
    # Executor-confirmed stop may precede, or never receive, worker acknowledgement.
    if record["binding"] is not None:
        check_binding(record["binding"], record, f"{name}.binding")
    if record["phase"] in {"Submitted", "Evaluating", "Accepted", "Rejected"}:
        require(record["binding"] is not None, f"{name}: submitted work requires a full binding")
    assessment = record["assessment"]
    if assessment is not None:
        fields(assessment, {"binding", "acceptance", "technical_result", "scientific_result", "reviewer", "receipt"}, f"{name}.assessment")
        require(record["phase"] in {"Evaluating", "Accepted", "Rejected"}, f"{name}: assessment is outside review phases")
        check_binding(assessment["binding"], record, f"{name}.assessment.binding")
        require(assessment["binding"] == record["binding"], f"{name}: assessment/candidate binding mismatch")
        require(assessment["acceptance"] in {"passed", "failed", "not_assessed"}, f"{name}: invalid acceptance")
        require(assessment["technical_result"] in {"pass", "fail", "not_assessed", "not_applicable"}, f"{name}: invalid technical result")
        require(assessment["scientific_result"] in {"supports", "weakens", "inconclusive", "invalid_experiment", "not_assessed", "not_applicable"}, f"{name}: invalid scientific result")
        require(text(assessment["reviewer"]) and text(assessment["receipt"]), f"{name}: assessment needs reviewer/receipt metadata")
    if record["phase"] == "Accepted":
        require(assessment is not None and assessment["acceptance"] == "passed", f"{name}: Accepted needs passed deliverable assessment")
        require(not record["blockers"], f"{name}: Accepted deliverable still has blockers")
        require(record["disposition"] != "active", f"{name}: Accepted deliverable needs terminal disposition")
        # Unresolved external effects can remain after an accepted failure report.
    if record["phase"] == "Rejected":
        require(assessment is not None and assessment["acceptance"] == "failed", f"{name}: Rejected needs failed deliverable assessment")
        require(record["disposition"] != "active", f"{name}: Rejected deliverable needs terminal disposition")
    require(isinstance(record["dependencies"], list), f"{name}: dependencies must be a list")
    seen = set()
    for dependency in record["dependencies"]:
        fields(dependency, {"task_id", "task_revision", "record_sha256"}, f"{name}.dependency")
        require(matches(ID, dependency["task_id"]), f"{name}: invalid prerequisite task ID")
        require(type(dependency["task_revision"]) is int and dependency["task_revision"] > 0, f"{name}: invalid prerequisite revision")
        require(matches(DIGEST, dependency["record_sha256"]), f"{name}: prerequisite must pin a record digest")
        target = (dependency["task_id"], dependency["task_revision"])
        require(target not in seen, f"{name}: duplicate prerequisite")
        seen.add(target)


def check_transition(previous, current):
    name = f"{current['task_id']}@{current['task_revision']}"
    old_phase, phase = previous["phase"], current["phase"]
    require(phase == old_phase or phase in PHASES[old_phase], f"{name}: illegal transition {old_phase} -> {phase}")
    require(current["task_kind"] == previous["task_kind"], f"{name}: task_kind changed; use a new task")
    if current["task_kind"] == "experiment":
        require(not (old_phase == "Investigating" and phase == "Submitted"), f"{name}: experiment requires Authorized/Implementing admission before submission")
    if current["task_spec"] != previous["task_spec"]:
        require(phase in {"Proposed", "Investigating"} and current["assessment"] is None, f"{name}: changed task definition needs investigation and fresh assessment")
    if current["binding"] != previous["binding"]:
        require(current["assessment"] is None, f"{name}: changed binding cannot retain acceptance; submit then reassess")
        require(phase != "Accepted", f"{name}: changed candidate cannot remain Accepted")
        if current["task_kind"] == "experiment":
            require(phase in {"Proposed", "Investigating", "Implementing"} or (old_phase == "Implementing" and phase == "Submitted"), f"{name}: experiment binding change requires investigation or admitted implementation/submission")
    before, after = previous["control"], current["control"]
    if before["unresolved_effects"] and not after["unresolved_effects"]:
        require(text(after["resolution_receipt"]), f"{name}: clearing unresolved effects needs a reconciliation receipt")
    if before["hold_requested"] and not after["hold_requested"]:
        require(text(after["resolution_receipt"]), f"{name}: releasing hold needs a decision receipt")
    if before["stop_requested"] and not after["stop_requested"]:
        require(before["stop_confirmed"] and not before["unresolved_effects"] and text(after["resolution_receipt"]), f"{name}: cannot clear unconfirmed stop or unresolved effects for resumption")
    entering_execution = phase != old_phase or (previous["disposition"] != "active" and current["disposition"] == "active")
    if entering_execution and phase in {"Authorized", "Implementing"}:
        require(current["disposition"] == "active", f"{name}: withdrawn work cannot enter execution")
        require(not current["blockers"] and not after["hold_requested"] and not after["stop_requested"] and not after["unresolved_effects"], f"{name}: admission/resumption blocked by blockers, hold, stop request, or unresolved effects")


def validate(envelopes):
    """Validate a complete supplied collection and return a deterministic summary."""
    require(bool(envelopes), "no coordination collections supplied")
    operations, tasks, indexed = {}, defaultdict(list), {}
    demonstration = None
    duplicates = 0
    count = 0
    for envelope in envelopes:
        fields(envelope, {"schema_version", "demonstration", "records"}, "collection", {"description"})
        require(type(envelope["schema_version"]) is int and envelope["schema_version"] == 1, "unsupported schema_version")
        require(type(envelope["demonstration"]) is bool, "demonstration must be boolean")
        if demonstration is None:
            demonstration = envelope["demonstration"]
        require(envelope["demonstration"] == demonstration, "cannot combine demonstration and actual records")
        require(isinstance(envelope["records"], list), "records must be a list")
        count += len(envelope["records"])
        require(count <= MAX_RECORDS, f"collection exceeds {MAX_RECORDS} records")
        for record in envelope["records"]:
            check_record(record, demonstration)
            operation = record["operation_id"]
            if operation in operations:
                require(canonical(operations[operation]) == canonical(record), f"operation {operation}: reused ID with different immutable payload")
                duplicates += 1
                continue
            operations[operation] = record
            key = (record["task_id"], record["task_revision"])
            require(key not in indexed, f"{key[0]}@{key[1]}: competing successors/revision conflict")
            indexed[key] = record
            tasks[key[0]].append(record)
    require(bool(operations), "collection contains no records")
    receipt_bindings = {}
    for task_id, history in tasks.items():
        history.sort(key=lambda record: record["task_revision"])
        for index, record in enumerate(history):
            require(record["task_revision"] == index + 1, f"{task_id}: incomplete/noncontiguous revision history")
            if index == 0:
                require(record["previous_record_sha256"] is None and record["phase"] == "Proposed", f"{task_id}: history must start Proposed at revision 1 with no previous hash")
            else:
                previous = history[index - 1]
                require(record["previous_record_sha256"] == record_hash(previous), f"{task_id}@{index + 1}: previous-record hash mismatch or fork")
                check_transition(previous, record)
            assessment = record["assessment"]
            if assessment:
                receipt = assessment["receipt"]
                bound = canonical(assessment["binding"])
                require(receipt not in receipt_bindings or receipt_bindings[receipt] == bound, f"{task_id}: assessment receipt reused for a different binding")
                receipt_bindings[receipt] = bound
    # Check graph intent before digests, so a malformed cycle gets a useful error.
    indegree = {key: 0 for key in indexed}
    outgoing = defaultdict(list)
    for key, record in indexed.items():
        if key[1] > 1:
            outgoing[(key[0], key[1] - 1)].append(key)
            indegree[key] += 1
        for dependency in record["dependencies"]:
            target = (dependency["task_id"], dependency["task_revision"])
            require(target in indexed, f"{key[0]}@{key[1]}: missing pinned prerequisite {target[0]}@{target[1]}")
            outgoing[target].append(key)
            indegree[key] += 1
    ready = deque(sorted(key for key, degree in indegree.items() if degree == 0))
    visited = 0
    while ready:
        key = ready.popleft()
        visited += 1
        for successor in outgoing[key]:
            indegree[successor] -= 1
            if indegree[successor] == 0:
                ready.append(successor)
    require(visited == len(indexed), "execution dependency cycle among pinned task revisions")
    for key, record in indexed.items():
        for dependency in record["dependencies"]:
            target = indexed[(dependency["task_id"], dependency["task_revision"])]
            require(dependency["record_sha256"] == record_hash(target), f"{key[0]}@{key[1]}: prerequisite digest mismatch")
            require(target["phase"] == "Accepted", f"{key[0]}@{key[1]}: prerequisite deliverable is not Accepted")
    rows = []
    for task_id in sorted(tasks):
        current = tasks[task_id][-1]
        outcome = current["assessment"]["scientific_result"] if current["assessment"] else "not_assessed"
        attention = list(current["blockers"])
        attention.extend(flag for flag in sorted(CONTROL_FLAGS - {"stop_acknowledged", "stop_confirmed"}) if current["control"][flag])
        rows.append(f"{task_id}@{current['task_revision']}: {current['phase']}/{current['disposition']}; scientific={outcome}; attention={', '.join(attention) or 'none'}")
    return {"demonstration": demonstration, "records": len(operations), "duplicates": duplicates, "tasks": rows}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="JSON files or directories; all supplied files form one collection")
    parser.add_argument("--examples", action="store_true", help="validate synthetic fixtures instead of operational records")
    args = parser.parse_args(argv)
    if args.examples and args.paths:
        parser.error("--examples cannot be combined with explicit paths")
    default_operational = not args.examples and not args.paths
    directory = Path(__file__).resolve().parent.parent / "harness/coordination" / ("examples" if args.examples else "records")
    paths = args.paths or [directory]
    try:
        files = []
        for path in paths:
            if default_operational and not path.exists():
                continue
            for file in path.rglob("*.json") if path.is_dir() else [path]:
                files.append(file)
                require(len(files) <= MAX_FILES, f"supply at most {MAX_FILES} JSON files")
        files.sort()
        if default_operational and not files:
            print(f"No operational coordination records found under {directory}; no operational validation performed.")
            return 0
        require(0 < len(files) <= MAX_FILES, f"supply 1 to {MAX_FILES} JSON files")
        remaining = MAX_BYTES
        envelopes = []
        for path in files:
            with path.open("rb") as stream:
                payload = stream.read(remaining + 1)
            require(len(payload) <= remaining, f"input exceeds {MAX_BYTES} bytes in total")
            remaining -= len(payload)
            envelopes.append(json.loads(payload, object_pairs_hook=unique_object))
        result = validate(envelopes)
        require(not default_operational or not result["demonstration"], "operational records directory cannot contain demonstration records")
        require(not args.examples or result["demonstration"], "--examples requires demonstration records")
    except (Invalid, OSError, UnicodeError, ValueError, TypeError, RecursionError) as error:
        print(f"Coordination records INVALID: {error}", file=sys.stderr)
        return 1
    label = "DEMONSTRATION ONLY" if result["demonstration"] else "SUPPLIED RECORDS ONLY"
    print(f"Coordination records consistent ({label}): {result['records']} unique records; {result['duplicates']} logical duplicates.")
    for row in result["tasks"]:
        print(row)
    print("No authentication, artifact-content verification, scientific validation, liveness, resource exclusion, or GitHub synchronization is established.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
