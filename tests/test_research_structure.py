"""Failure-oriented tests for structural research-record validation."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_research.py"
SPEC = importlib.util.spec_from_file_location("check_research", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class ResearchStructureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in CHECKER.REQUIRED_FILES:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Fixture\n", encoding="utf-8")
        self.hypothesis = self.root / "research" / "HYP-0001.md"
        self.hypothesis.parent.mkdir()
        self.hypothesis.write_text("Fixture hypothesis\n", encoding="utf-8")
        self.manifest = {
            "id": "EXP-0001",
            "status": "planned",
            "hypothesis": "HYP-0001",
            "question": "Does a candidate improve transfer?",
            "baseline": "A deterministic comparator",
            "candidate": "A proposed representation",
            "metrics": ["task_success"],
            "dataset": {"source": "TBD", "holdout": "TBD", "split_hash": None},
            "protocol": {
                "random_seeds": [],
                "sample_count": None,
                "resource_caps": "TBD",
                "pre_registered": False,
            },
            "results": None,
        }

    def write_manifest(self, manifest=None, directory="EXP-0001"):
        path = self.root / "experiments" / directory / "manifest.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.manifest if manifest is None else manifest), encoding="utf-8"
        )
        return path

    def assert_invalid(self, message):
        with self.assertRaisesRegex(CHECKER.ResearchStructureError, message):
            CHECKER.validate(self.root)

    def test_planning_scaffold_with_null_results_is_valid(self):
        path = self.write_manifest()
        self.assertEqual(CHECKER.validate(self.root), [path])

    def test_every_discovered_experiment_is_checked(self):
        first = self.write_manifest()
        second_manifest = dict(self.manifest, id="EXP-0002")
        second = self.write_manifest(second_manifest, "EXP-0002")
        self.assertEqual(CHECKER.validate(self.root), [first, second])
        second.write_text("{", encoding="utf-8")
        self.assert_invalid("EXP-0002/manifest.json: cannot read valid JSON")

    def test_missing_manifest_is_an_error(self):
        self.write_manifest()
        (self.root / "experiments" / "EXP-0002").mkdir()
        self.assert_invalid("missing experiment manifest")

    def test_no_experiments_is_an_error(self):
        self.assert_invalid("no experiment directories")

    def test_missing_hypothesis_is_an_error(self):
        self.write_manifest()
        self.hypothesis.unlink()
        self.assert_invalid("referenced hypothesis does not exist")

    def test_cross_directory_identity_is_an_error(self):
        self.write_manifest(directory="EXP-0002")
        self.assert_invalid("id EXP-0001 does not match directory EXP-0002")

    def test_duplicate_ids_are_reported(self):
        self.write_manifest()
        self.write_manifest(directory="EXP-0002")
        self.assert_invalid("duplicate experiment id EXP-0001")

    def test_hypothesis_cannot_be_an_arbitrary_path(self):
        self.manifest["hypothesis"] = "../AGENTS"
        self.write_manifest()
        self.assert_invalid("hypothesis must have the form")

    def test_unrecognized_lifecycle_is_an_error(self):
        self.manifest["status"] = "hypothesis-proven"
        self.write_manifest()
        self.assert_invalid("unrecognized lifecycle state")

    def test_planned_results_must_be_null_even_for_empty_object(self):
        for result in ({}, [], {"summary": "Claimed outcome", "evidence": ["run-1.json"]}):
            with self.subTest(result=result):
                self.manifest["results"] = result
                self.write_manifest()
                self.assert_invalid("planned experiments must have null results")

    def test_completed_without_result_record_is_invalid(self):
        self.manifest["status"] = "completed"
        self.write_manifest()
        self.assert_invalid("completed experiments require a structured result record")

    def test_completed_negative_and_inconclusive_pilots_are_valid(self):
        for conclusion in ("negative", "inconclusive"):
            with self.subTest(conclusion=conclusion):
                self.manifest["status"] = "completed"
                self.manifest["protocol"]["kind"] = "exploratory_pilot"
                self.manifest["results"] = {
                    "summary": "Pilot produced no evidence of the proposed advantage.",
                    "evidence": ["runs/pilot-1/raw.json"],
                    "conclusion": conclusion,
                }
                self.write_manifest()
                self.assertFalse(self.manifest["protocol"]["pre_registered"])
                CHECKER.validate(self.root)

    def test_partial_results_survive_interruption_or_supersession(self):
        for state in ("running", "incomplete", "aborted", "cancelled", "superseded"):
            for result in (None, {
                "summary": "Partial observations; no complete comparison.",
                "evidence": ["runs/partial/log.json"],
            }):
                with self.subTest(state=state, result=result):
                    self.manifest["status"] = state
                    self.manifest["results"] = result
                    self.write_manifest()
                    CHECKER.validate(self.root)

    def test_result_shape_is_checked_without_requiring_positive_conclusion(self):
        for result, message in (
            ([], "results must be null or an object"),
            ({"summary": "", "evidence": ["log"]}, "results.summary"),
            ({"summary": "Partial run", "evidence": []}, "results.evidence"),
            ({"summary": "Partial run", "evidence": [None]}, "results.evidence"),
            (
                {"summary": "Partial run", "evidence": ["log"], "conclusion": False},
                "results.conclusion",
            ),
        ):
            with self.subTest(result=result):
                self.manifest["status"] = "running"
                self.manifest["results"] = result
                self.write_manifest()
                self.assert_invalid(message)

    def test_required_types_reject_boolean_sample_count_and_seed(self):
        for key, value, message in (
            ("sample_count", True, "protocol.sample_count"),
            ("random_seeds", [True], "protocol.random_seeds"),
            ("pre_registered", "false", "protocol.pre_registered"),
            ("resource_caps", [], "protocol.resource_caps"),
        ):
            with self.subTest(key=key):
                previous = self.manifest["protocol"][key]
                self.manifest["protocol"][key] = value
                self.write_manifest()
                self.assert_invalid(message)
                self.manifest["protocol"][key] = previous

    def test_required_fields_and_object_shapes(self):
        for field, replacement in (
            ("metrics", "task_success"),
            ("dataset", []),
            ("protocol", []),
            ("question", " "),
        ):
            with self.subTest(field=field):
                manifest = dict(self.manifest)
                manifest[field] = replacement
                self.write_manifest(manifest)
                self.assert_invalid(field)
        del self.manifest["results"]
        self.write_manifest()
        self.assert_invalid("missing required field: results")

    def test_duplicate_keys_and_non_json_numbers_are_rejected(self):
        path = self.write_manifest()
        for content in ('{"status":"planned","status":"completed"}', '{"sample":NaN}'):
            with self.subTest(content=content):
                path.write_text(content, encoding="utf-8")
                self.assert_invalid("cannot read valid JSON")

    def test_extra_protocol_fields_do_not_freeze_architecture(self):
        self.manifest["protocol"]["future_representation"] = {"kind": "new-candidate"}
        self.manifest["future_field"] = [1, 2, 3]
        self.write_manifest()
        CHECKER.validate(self.root)

    def test_cli_reports_invalid_structure_without_success_output(self):
        path = self.write_manifest()
        path.write_text("not JSON", encoding="utf-8")
        output, error = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = CHECKER.main(["--root", str(self.root)])
        self.assertEqual(code, 1)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("cannot read valid JSON", error.getvalue())


if __name__ == "__main__":
    unittest.main()
