#!/usr/bin/env python3
"""Validate research record structure, not evidence, authority, or conclusions.

The current manifests may remain exploratory. Completing an experiment does not
require preregistration or a positive scientific conclusion. Evidence references
are checked as strings; this script does not fetch or certify their contents.
"""

import argparse
import json
from pathlib import Path
import re
import sys


REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "docs/methodology.md",
    "wiki/Home.md",
)
EXPERIMENT_ID = re.compile(r"EXP-[0-9]{4,}\Z")
HYPOTHESIS_ID = re.compile(r"HYP-[0-9]{4,}\Z")
LIFECYCLE_STATES = frozenset(
    {"planned", "running", "completed", "incomplete", "aborted", "cancelled", "superseded"}
)


class ResearchStructureError(ValueError):
    """One or more records do not satisfy the structural contract."""


def _nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def _string_list(value):
    return isinstance(value, list) and bool(value) and all(
        _nonempty_string(item) for item in value
    )


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError(f"non-JSON numeric constant: {value}")


def _check_manifest(manifest, directory_name, root, report):
    if not isinstance(manifest, dict):
        report("manifest must be a JSON object")
        return

    for field in (
        "id", "status", "hypothesis", "question", "baseline", "candidate",
        "metrics", "dataset", "protocol", "results",
    ):
        if field not in manifest:
            report(f"missing required field: {field}")

    experiment_id = manifest.get("id")
    if not isinstance(experiment_id, str) or not EXPERIMENT_ID.fullmatch(experiment_id):
        report("id must have the form EXP-0001 (at least four digits)")
    elif experiment_id != directory_name:
        report(f"id {experiment_id} does not match directory {directory_name}")

    status = manifest.get("status")
    if not isinstance(status, str) or status not in LIFECYCLE_STATES:
        report(f"unrecognized lifecycle state: {status!r}")

    hypothesis = manifest.get("hypothesis")
    if not isinstance(hypothesis, str) or not HYPOTHESIS_ID.fullmatch(hypothesis):
        report("hypothesis must have the form HYP-0001 (at least four digits)")
    elif not (root / "research" / f"{hypothesis}.md").is_file():
        report(f"referenced hypothesis does not exist: research/{hypothesis}.md")

    for field in ("question", "baseline", "candidate"):
        if not _nonempty_string(manifest.get(field)):
            report(f"{field} must be a nonempty string")
    if not _string_list(manifest.get("metrics")):
        report("metrics must be a nonempty list of nonempty strings")

    dataset = manifest.get("dataset")
    if not isinstance(dataset, dict):
        report("dataset must be an object")
    else:
        for field in ("source", "holdout"):
            if not _nonempty_string(dataset.get(field)):
                report(f"dataset.{field} must be a nonempty string")
        if "split_hash" not in dataset:
            report("dataset.split_hash is required (null is allowed while unresolved)")
        elif dataset["split_hash"] is not None and not _nonempty_string(dataset["split_hash"]):
            report("dataset.split_hash must be null or a nonempty string")

    protocol = manifest.get("protocol")
    if not isinstance(protocol, dict):
        report("protocol must be an object")
    else:
        if not isinstance(protocol.get("pre_registered"), bool):
            report("protocol.pre_registered must be a boolean")
        seeds = protocol.get("random_seeds")
        if not isinstance(seeds, list) or not all(type(seed) is int for seed in seeds):
            report("protocol.random_seeds must be a list of integers")
        if "sample_count" not in protocol:
            report("protocol.sample_count is required (null is allowed while unresolved)")
        else:
            sample_count = protocol["sample_count"]
            if sample_count is not None and not (type(sample_count) is int and sample_count > 0):
                report("protocol.sample_count must be null or a positive integer")
        caps = protocol.get("resource_caps")
        if not (_nonempty_string(caps) or isinstance(caps, dict) and bool(caps)):
            report("protocol.resource_caps must be a nonempty string or object")

    if "results" not in manifest:
        return
    results = manifest["results"]
    if status == "planned" and results is not None:
        report("planned experiments must have null results")
    if status == "completed" and results is None:
        report("completed experiments require a structured result record")
    if results is None:
        return
    if not isinstance(results, dict):
        report("results must be null or an object")
        return
    if not _nonempty_string(results.get("summary")):
        report("results.summary must be a nonempty string")
    if not _string_list(results.get("evidence")):
        report("results.evidence must be a nonempty list of evidence-reference strings")
    if "conclusion" in results and not _nonempty_string(results["conclusion"]):
        report("results.conclusion, when present, must be a nonempty string")


def validate(root):
    """Validate a repository root and return the discovered manifest paths.

    Raises ResearchStructureError with all detected structural errors. Additional
    record fields are permitted so task-specific protocols can evolve separately.
    No files are written and no evidence or remote services are accessed.
    """
    root = Path(root)
    errors = []
    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            errors.append(f"missing required artifact: {name}")

    experiments = root / "experiments"
    directories = sorted(experiments.glob("EXP-*")) if experiments.is_dir() else []
    if not directories:
        errors.append("no experiment directories found under experiments/EXP-*")

    manifests = []
    seen_ids = {}
    for directory in directories:
        relative = directory.relative_to(root)
        if not directory.is_dir() or not EXPERIMENT_ID.fullmatch(directory.name):
            errors.append(f"invalid experiment directory: {relative}")
            continue
        path = directory / "manifest.json"
        relative = path.relative_to(root)
        if not path.is_file():
            errors.append(f"missing experiment manifest: {relative}")
            continue
        manifests.append(path)
        try:
            manifest = json.loads(
                path.read_text(encoding="utf-8"),
                object_pairs_hook=_unique_object,
                parse_constant=_reject_constant,
            )
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"{relative}: cannot read valid JSON: {error}")
            continue

        if isinstance(manifest, dict) and isinstance(manifest.get("id"), str):
            experiment_id = manifest["id"]
            if experiment_id in seen_ids:
                errors.append(
                    f"{relative}: duplicate experiment id {experiment_id}; "
                    f"already used by {seen_ids[experiment_id]}"
                )
            else:
                seen_ids[experiment_id] = relative

        def report(message):
            errors.append(f"{relative}: {message}")

        _check_manifest(manifest, directory.name, root, report)

    if errors:
        raise ResearchStructureError("\n".join(errors))
    return manifests


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parent.parent,
        help="repository root to inspect (defaults to this script's repository)",
    )
    args = parser.parse_args(argv)
    try:
        manifests = validate(args.root)
    except ResearchStructureError as error:
        print(f"Research structure invalid:\n{error}", file=sys.stderr)
        return 1
    print(
        f"Research structure valid across {len(manifests)} experiment manifests; "
        "no scientific, authorization, or Rust verification."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
