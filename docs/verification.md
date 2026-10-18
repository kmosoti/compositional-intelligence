# Verification and trust

Distinguish compiler pass, unit/property tests, numerical conformance, resource benchmarks, sandbox isolation, final integration checks, and scientific validation. None substitutes for the others.

Miri examines executions and does not prove Rust soundness in general. Simulated instruction/cache counts are not measured wall-clock performance. `repr(transparent)` constrains representation, not zero-cost behavior.

Workers must not control evaluator images, hidden tests, production signing keys or authoritative acceptance records. Test the final integrated tree: independently passing changes can interact badly after merging.

Acceptance reports must list exact executed commands and resulting evidence, including when a test was not run. No hidden success claims.
