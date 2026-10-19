# Coordination records and offline checks

The current operating mode is manual coordination with deterministic, read-only validation. Start with the [coordination contract](../../docs/coordination.md), its [research appraisal](../../docs/research/github-coordination-review.md), and [bounded adoption record](../../docs/coordination-adoption.md). These checks are instruments for detecting inconsistent records; an autonomous coordinator, GitHub Project writer, resource controller, and evaluator service remain unimplemented.

## Run the checks

From the repository root, using Python 3 and its standard library:

```sh
python3 -B scripts/check_research.py
python3 -B scripts/check_coordination.py
python3 -B scripts/check_coordination.py --examples
python3 -B -m unittest discover -s tests -v
```

The first command discovers and validates every `experiments/EXP-*/manifest.json`. The second recursively discovers real coordination records under [records/](records/README.md). That directory initially contains no operational JSON; the command explicitly reports that no operational validation was performed. The third separately checks the synthetic example collection. The last runs failure-trace and structural regression tests; temporary test data are not research results.

Additional explicit paths can be checked together:

```sh
python3 -B scripts/check_coordination.py path/to/records.json path/to/another-directory/
```

Supply a complete relevant history, including pinned prerequisites. Different files are one collection, not independent verdicts. Demo and operational envelopes cannot be mixed. See the [version 1 format, transitions, bounds, and examples](examples/README.md) before writing a record. That document and the checker are the precise executable-model contract; the higher-level coordination document also describes manual and future operational responsibilities that the checker cannot enforce.

## Experiment manifest lifecycle

The research checker discovers experiments instead of requiring the first experiment to remain planned forever. It permits task-specific additional fields and checks these common fields: matching experiment ID, existing hypothesis reference, nonempty question/baseline/candidate/metrics, dataset metadata, protocol metadata, lifecycle, and result shape. Duplicate JSON keys and non-JSON numeric constants are rejected.

| `status` | Minimum structural result rule |
| --- | --- |
| `planned` | `results: null` |
| `running` | Null or a structured partial result |
| `completed` | A structured result object |
| `incomplete`, `aborted`, `cancelled`, `superseded` | Null or a structured partial/final result |

A result object has the following minimum shape:

```json
{
  "summary": "A nonempty account of the observed outcome and its limits.",
  "evidence": ["A retained evidence reference; not an invented result."],
  "conclusion": "Optional nonempty interpretation, including negative or inconclusive findings."
}
```

This is a shape illustration only. It is not an experiment result to paste into a live manifest. `summary` and a nonempty list of nonempty `evidence` references are required; `conclusion` is optional free text. The validator does not retrieve references or certify the claims. Detailed raw outcomes, baseline/candidate costs, input and environment identities, uncertainty, and deviations belong in the linked result artifacts under the applicable [scientific method](../../docs/methodology.md).

`protocol.pre_registered` must be an honest Boolean. Completed exploratory work is allowed; marking it completed does not retroactively preregister it. Protocol random seeds must be integer lists, sample count null or positive, and resource caps a nonempty string or object. These permissive shapes allow planning and distinct experimental designs; they do not establish that an executed comparison had adequate controls or statistical power. Protected evaluation material remains in its permitted location.

Experiment lifecycle and coordination phase describe different things. An experiment result can be completed while its report awaits independent acceptance. A coordination task can accept an honest invalid-attempt report without making the underlying measurement valid. Architectural adoption remains a separate research decision.

## What the coordination checker exercises

The checker compares exact submission/assessment bindings, per-task revisions and predecessor hashes, logical operation identity, modeled phase transitions, declared hold/stop/effect facts, and versioned prerequisites. The synthetic negative example follows the admitted experiment path through independent-assessment metadata to an accepted deliverable whose scientific result weakens the hypothesis. Metadata in a fixture is not an actual independent review.

The tests include conflicting/replayed operations, missing/forked history, stale acceptance, task-definition amendments, admission bypasses, invalid rejection states, control-state contradictions, prerequisite failures, valid iterative dependencies, malformed input, and accidental mixing of demonstrations with operational records.

These tests do not exercise GitHub transport, process termination, actual reviewer identity, resource fencing, evidence retrieval, leakage detection, statistical validity, or the effectiveness of multi-agent coordination. Implementing any of those capabilities needs its own bounded contract and appropriate tests. Passing this suite is not a model benchmark or an intelligence result.
