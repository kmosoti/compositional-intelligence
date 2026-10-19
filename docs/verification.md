# Verification and trust

Distinguish compiler pass, unit/property tests, numerical conformance, resource benchmarks, sandbox isolation, final integration checks, and scientific validation. None substitutes for the others.

Miri examines executions and does not prove Rust soundness in general. Simulated instruction/cache counts are not measured wall-clock performance. `repr(transparent)` constrains representation, not zero-cost behavior.

Workers must not control evaluator images, hidden tests, production signing keys or authoritative acceptance records. Test the final integrated tree: independently passing changes can interact badly after merging.

Acceptance reports must list exact executed commands and resulting evidence, including when a test was not run. No hidden success claims.

## Research and coordination records

Acceptance applies to the exact submitted task specification, candidate, protocol, evaluator, inputs, environment, and analysis where relevant. A change to one of these requires a new applicability assessment; retain the historical observation and its original scope. Use reasoned not-applicable entries for dimensions a non-experimental task does not use. Do not fabricate a benchmark or dataset to fill a template.

The [offline record checks](../harness/coordination/README.md) validate structure, recorded transitions, identity matching, and supplied dependency history. They do not fetch evidence, authenticate reviewers, enforce independent control, fence resources, or establish scientific truth. A passing structural check and a completed task do not establish that an architecture should be adopted.

Protect holdouts and evaluator-controlled material throughout review. Coordination records may identify restricted artifacts without exposing their contents. Recheck the integrated candidate where independently valid edits can interact.
