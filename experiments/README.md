# Experiment registry

Define a protocol and baseline; preregister confirmatory comparisons and label exploratory work explicitly. Store manifests without claiming execution. Results must include machine/software identifiers, dataset hashes, seeds, raw outcomes, baseline and candidate costs, uncertainties and negative findings.

Planned experiment manifests use `status: planned`. No result files exist yet.

| Experiment | Protocol | Status and unresolved gate |
| --- | --- | --- |
| [EXP-0001](EXP-0001/manifest.json) | Initial retrieval comparison | Planned; original scaffold retained |
| [EXP-0002](EXP-0002/manifest.json) | [Reusable abstraction and causal transfer](EXP-0002/protocol.md) | Planned; implementation, splits, sample-size decision, and budgets must be frozen |
| [EXP-0003](EXP-0003/manifest.json) | [Functional coordination](EXP-0003/protocol.md) | Planned; control policies and evaluation conditions must be frozen |
| [EXP-0004](EXP-0004/manifest.json) | [Retained competence](EXP-0004/protocol.md) | Planned; learner, retained state, assignment, and evaluation schedule must be frozen |

An ID does not mean preregistration or execution. Exploratory pilots may resolve feasibility and protocol choices, but their data are not reused as unseen confirmatory evidence. Freeze a comparison, not the project's future architecture. See the [research program](../docs/research-program.md).

The [manifest and coordination guide](../harness/coordination/README.md) documents the common lifecycle/result structure checked in CI. Completed negative, inconclusive, and exploratory results are permitted when honestly recorded. Structural validity does not establish independent acceptance or scientific adoption.
