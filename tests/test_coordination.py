"""Adversarial traces for the offline consistency model; no real coordination."""

import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("check_coordination", ROOT / "scripts/check_coordination.py")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


def example():
    return json.loads((ROOT / "harness/coordination/examples/completed-negative.json").read_text())


def rechain(envelope):
    histories = {}
    for record in envelope["records"]:
        histories.setdefault(record["task_id"], []).append(record)
    for history in histories.values():
        history.sort(key=lambda item: item["task_revision"])
        for index, record in enumerate(history):
            record["previous_record_sha256"] = CHECK.record_hash(history[index - 1]) if index else None
    return envelope


def append(envelope, phase, **changes):
    record = copy.deepcopy(envelope["records"][-1])
    record.update(task_revision=record["task_revision"] + 1, phase=phase, disposition="active", assessment=None)
    record["operation_id"] = f"{record['task_id']}-r{record['task_revision']}"
    record.update(changes)
    envelope["records"].append(record)
    rechain(envelope)
    return record


def renamed(envelope, name):
    result = copy.deepcopy(envelope)
    for record in result["records"]:
        record["task_id"] = name
        record["operation_id"] = f"{name}-r{record['task_revision']}"
    return rechain(result)


def pin(record):
    return {"task_id": record["task_id"], "task_revision": record["task_revision"], "record_sha256": CHECK.record_hash(record)}


class CoordinationTraceTests(unittest.TestCase):
    def rejects(self, envelope, message):
        with self.assertRaisesRegex(CHECK.Invalid, message):
            CHECK.validate([envelope])

    def test_completed_negative_and_inconclusive_are_accepted_deliverables(self):
        for result in ("weakens", "inconclusive"):
            data = example()
            for record in data["records"]:
                if record["assessment"]:
                    record["assessment"]["scientific_result"] = result
            summary = CHECK.validate([rechain(data)])
            self.assertIn(f"Accepted/completed; scientific={result}", summary["tasks"][0])

    def test_invalid_attempt_can_complete_while_effects_remain_unresolved(self):
        data = example()
        for record in data["records"][-2:]:
            record["assessment"]["scientific_result"] = "invalid_experiment"
            record["assessment"]["technical_result"] = "fail"
            record["control"]["unresolved_effects"] = True
        summary = CHECK.validate([rechain(data)])
        self.assertIn("Accepted/completed; scientific=invalid_experiment", summary["tasks"][0])
        self.assertIn("unresolved_effects", summary["tasks"][0])
        append(data, "Investigating")
        append(data, "Authorized")
        self.rejects(data, "resumption blocked")

    def test_clock_skew_and_out_of_order_transport_do_not_choose_a_winner(self):
        data = example()
        data["records"][1]["source_reported_at"] = "2030-01-01T00:00:00Z"
        rechain(data)
        ordered = CHECK.validate([data])
        data["records"].reverse()
        self.assertEqual(ordered, CHECK.validate([data]))

    def test_physical_duplicate_is_one_logical_operation(self):
        data = example()
        data["records"].append(copy.deepcopy(data["records"][0]))
        summary = CHECK.validate([data])
        self.assertEqual((summary["records"], summary["duplicates"]), (7, 1))

    def test_same_operation_id_with_changed_payload_conflicts(self):
        data = example()
        duplicate = copy.deepcopy(data["records"][0])
        duplicate["note"] = "A later writer changed the original operation."
        data["records"].append(duplicate)
        self.rejects(data, "reused ID with different")

    def test_two_successors_of_one_revision_conflict(self):
        data = example()
        competitor = copy.deepcopy(data["records"][1])
        competitor["operation_id"] = "competing-operation"
        data["records"].append(competitor)
        self.rejects(data, "competing successors")

    def test_deleted_or_edited_history_does_not_silently_reconstruct(self):
        data = example()
        data["records"].pop(1)
        self.rejects(data, "incomplete/noncontiguous")
        data = example()
        data["records"][1]["note"] = "Changed after acceptance."
        self.rejects(data, "previous-record hash mismatch")

    def test_candidate_change_cannot_reuse_old_assessment(self):
        data = example()
        data["records"][-1]["binding"]["candidate"] = "sha256:" + "f" * 64
        self.rejects(data, "assessment/candidate binding mismatch")

    def test_mutable_task_definition_cannot_retain_old_acceptance(self):
        data = example()
        data["records"][-1]["task_spec"] = "sha256:" + "f" * 64
        self.rejects(data, "task_spec differs")

    def test_same_receipt_cannot_be_relabelled_for_new_inputs(self):
        data = example()
        changed = copy.deepcopy(data["records"][-1]["binding"])
        changed["inputs"] = "sha256:" + "e" * 64
        append(data, "Investigating", binding=changed)
        append(data, "Authorized")
        append(data, "Implementing")
        append(data, "Submitted")
        assessment = copy.deepcopy(next(record["assessment"] for record in data["records"] if record["assessment"]))
        assessment["binding"] = changed
        append(data, "Evaluating", assessment=assessment)
        self.rejects(data, "receipt reused for a different binding")

    def test_executor_stop_does_not_require_worker_acknowledgement(self):
        data = example()
        for record in data["records"][4:]:
            record["control"].update(stop_requested=True, stop_confirmed=True, stop_acknowledged=False)
        CHECK.validate([rechain(data)])

    def test_acknowledgement_is_not_confirmation_for_resumption(self):
        data = example()
        data["records"][-1]["control"].update(stop_requested=True, stop_acknowledged=True, stop_confirmed=False)
        rechain(data)
        resumed = append(data, "Investigating")
        resumed["control"].update(stop_requested=False, stop_acknowledged=False, resolution_receipt="demo://request-ack")
        self.rejects(data, "cannot clear unconfirmed stop")

    def test_unresolved_effects_cannot_be_cleared_without_reconciliation_record(self):
        data = example()
        data["records"][-2]["control"]["unresolved_effects"] = True
        self.rejects(rechain(data), "clearing unresolved effects needs")

    def test_holds_block_new_execution_but_do_not_assert_a_stopped_process(self):
        data = example()
        data["records"] = data["records"][:2]
        append(data, "Authorized")["control"]["hold_requested"] = True
        self.rejects(data, "resumption blocked")

    def test_future_unresolved_prerequisites_and_withdrawal_need_no_fake_result(self):
        data = example()
        data["records"] = data["records"][:1]
        data["records"][0]["blockers"] = ["Await a future evaluator investigation; no accepted artifact exists."]
        data["records"][0]["disposition"] = "cancelled"
        CHECK.validate([data])
        append(data, "Authorized", disposition="active")
        self.rejects(data, "resumption blocked")

    def test_same_phase_reactivation_of_cancelled_work_still_checks_blockers(self):
        data = example()
        data["records"] = data["records"][:2]
        append(data, "Authorized")
        append(data, "Authorized", disposition="cancelled", blockers=["resource outcome unknown"])
        append(data, "Authorized", disposition="active")
        self.rejects(data, "resumption blocked")

    def test_missing_or_unaccepted_pinned_execution_prerequisite_is_error(self):
        data = example()
        data["records"][0]["dependencies"] = [{"task_id": "DEMO-MISSING", "task_revision": 1, "record_sha256": "0" * 64}]
        self.rejects(rechain(data), "missing pinned prerequisite")
        data = example()
        data["records"][-1]["dependencies"] = [pin(data["records"][0])]
        self.rejects(data, "prerequisite deliverable is not Accepted")

    def test_prerequisite_digest_is_checked(self):
        upstream = renamed(example(), "DEMO-UPSTREAM")
        data = example()
        data["records"][0]["dependencies"] = [pin(upstream["records"][-1])]
        data["records"][0]["dependencies"][0]["record_sha256"] = "0" * 64
        rechain(data)
        with self.assertRaisesRegex(CHECK.Invalid, "prerequisite digest mismatch"):
            CHECK.validate([upstream, data])

    def test_versioned_research_iterations_do_not_make_a_false_dependency_cycle(self):
        first, second = renamed(example(), "DEMO-A"), renamed(example(), "DEMO-B")
        first_done, second_done = pin(first["records"][-1]), pin(second["records"][-1])
        append(first, "Investigating", dependencies=[second_done])
        append(second, "Investigating", dependencies=[first_done])
        CHECK.validate([first, second])

    def test_concrete_execution_cycle_fails_but_conceptual_cycles_are_allowed(self):
        first, second = renamed(example(), "DEMO-A"), renamed(example(), "DEMO-B")
        first["records"], second["records"] = first["records"][:1], second["records"][:1]
        first["records"][0]["related"] = ["DEMO-B"]
        second["records"][0]["related"] = ["DEMO-A"]
        CHECK.validate([first, second])
        first["records"][0]["dependencies"] = [pin(second["records"][0])]
        second["records"][0]["dependencies"] = [pin(first["records"][0])]
        with self.assertRaisesRegex(CHECK.Invalid, "execution dependency cycle"):
            CHECK.validate([first, second])

    def test_prerequisite_on_own_future_revision_is_a_causal_cycle(self):
        data = example()
        data["records"][0]["dependencies"] = [pin(data["records"][-1])]
        self.rejects(rechain(data), "execution dependency cycle")

    def test_reasoned_nonapplicability_is_allowed_only_outside_experiments(self):
        data = example()
        for record in data["records"]:
            record["task_kind"] = "investigation"
            if record["binding"]:
                record["binding"]["environment"] = "not_applicable: literature synthesis with no execution environment"
            if record["assessment"]:
                record["assessment"]["binding"] = copy.deepcopy(record["binding"])
        CHECK.validate([rechain(data)])
        for record in data["records"]:
            record["task_kind"] = "experiment"
        self.rejects(rechain(data), "expected immutable ID")

    def test_experiment_cannot_use_the_investigation_submission_shortcut(self):
        data = example()
        data["records"] = [record for record in data["records"] if record["phase"] not in {"Authorized", "Implementing"}]
        for index, record in enumerate(data["records"], 1):
            record["task_revision"] = index
        self.rejects(rechain(data), "experiment requires Authorized/Implementing")
        for record in data["records"]:
            record["task_kind"] = "investigation"
        CHECK.validate([rechain(data)])

    def test_changed_experiment_spec_requires_fresh_admission(self):
        data = example()
        data["records"] = data["records"][:4]
        new_spec = "sha256:" + "c" * 64
        new_binding = copy.deepcopy(data["records"][-1]["binding"])
        new_binding["task_spec"] = new_spec
        append(data, "Investigating", task_spec=new_spec, binding=None)
        bad = copy.deepcopy(data)
        append(bad, "Submitted", binding=new_binding)
        self.rejects(bad, "experiment requires Authorized/Implementing")
        append(data, "Authorized")
        append(data, "Implementing")
        append(data, "Submitted", binding=new_binding)
        CHECK.validate([data])

    def test_same_phase_experiment_submission_cannot_replace_candidate_without_execution(self):
        data = example()
        data["records"] = data["records"][:5]
        new_binding = copy.deepcopy(data["records"][-1]["binding"])
        new_binding["candidate"] = "sha256:" + "a" * 64
        append(data, "Submitted", binding=new_binding)
        self.rejects(data, "binding change requires investigation or admitted")

    def test_rejected_requires_failed_scoped_deliverable_assessment(self):
        data = example()
        data["records"][-1]["phase"] = "Rejected"
        self.rejects(data, "Rejected needs failed deliverable assessment")
        data["records"][-1]["assessment"]["acceptance"] = "failed"
        CHECK.validate([data])
        data = example()
        data["records"] = data["records"][:1]
        append(data, "Rejected", disposition="completed")
        self.rejects(data, "requires a full binding")

    def test_plausible_reviewer_metadata_is_not_authenticated_by_this_model(self):
        data = example()
        for record in data["records"]:
            if record["assessment"]:
                record["assessment"]["reviewer"] = "unverified claim of owner approval"
        # Intentional scope limit: validity of this string is never established.
        CHECK.validate([rechain(data)])

    def test_schema_time_format_and_input_size_are_bounded(self):
        data = example()
        data["schema_version"] = 2
        self.rejects(data, "unsupported schema")
        data = example()
        data["records"][0]["observed_at"] = "2026-10-19T00:01:01-05:00"
        self.rejects(data, "ISO UTC")
        data = example()
        data["records"] = [data["records"][0]] * (CHECK.MAX_RECORDS + 1)
        self.rejects(data, "exceeds")

    def test_cli_rejects_duplicate_json_keys_without_writing_records(self):
        payload = '{"schema_version":1,"schema_version":2,"demonstration":true,"records":[]}'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.json"
            path.write_text(payload)
            errors = io.StringIO()
            with contextlib.redirect_stderr(errors):
                status = CHECK.main([str(path)])
            self.assertEqual(status, 1)
            self.assertIn("duplicate JSON object key", errors.getvalue())
            self.assertEqual(path.read_text(), payload)

    def test_default_checks_nested_operational_records_and_reports_empty_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(CHECK, "__file__", str(root / "scripts/check_coordination.py")):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(CHECK.main([]), 0)
                self.assertIn("no operational validation performed", output.getvalue())
                nested = root / "harness/coordination/records/task/history"
                nested.mkdir(parents=True)
                (nested / "bad.json").write_text(json.dumps({"schema_version": 2, "demonstration": False, "records": []}))
                errors = io.StringIO()
                with contextlib.redirect_stderr(errors):
                    self.assertEqual(CHECK.main([]), 1)
                self.assertIn("unsupported schema_version", errors.getvalue())

    def test_demonstrations_cannot_satisfy_operational_discovery(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records = root / "harness/coordination/records"
            records.mkdir(parents=True)
            (records / "misplaced-example.json").write_text(json.dumps(example()))
            with patch.object(CHECK, "__file__", str(root / "scripts/check_coordination.py")):
                errors = io.StringIO()
                with contextlib.redirect_stderr(errors):
                    self.assertEqual(CHECK.main([]), 1)
                self.assertIn("cannot contain demonstration records", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
