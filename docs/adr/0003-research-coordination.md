# ADR 0003: Versioned research coordination with a manual baseline

**Status:** Accepted as the scoped coordination baseline; operational benefits remain unmeasured.

**Date:** 2026-10-19.

## Context

The owner supplied a project-neutral GitHub Project coordination playbook and asked for research and maturation for compositional-intelligence. The playbook separates a coordination protocol from its GitHub projection and human interface. The repository currently has process instructions and research plans, but no autonomous execution/controller service or bound Project configuration.

Three risks are concrete. Generic completion rules can make a valid negative experiment appear unfinished. Mutable comments cannot by themselves preserve the accepted research record. The existing structural checker permanently requires EXP-0001 to remain planned and ignores later experiments, making the project's initial state an accidental invariant.

The project needs useful consistency checks while retaining the freedom to revise code, protocols, hypotheses, and coordination machinery under [ADR 0002](0002-research-governs-implementation.md).

## Decision

1. Use manual coordination under the existing worker/evaluator/controller authority model. A named coordinator serializes acceptance and integration for the bounded task; this does not impose a permanent agent hierarchy or inference router.
2. Preserve accepted coordination and scientific records in versioned repository artifacts. Project fields and comments are projections, reports, and navigation. Their state does not independently authorize work or establish acceptance.
3. Keep phase, blockers/control observations, technical assessment, scientific result, and task disposition distinct. Accepted research may have negative, inconclusive, or invalid-run findings. Adoption is a further research decision.
4. Bind acceptance to the task specification and exact candidate/protocol/evaluator/input/environment/analysis identities. Preserve previous observations when a candidate or interpretation changes.
5. Add a small offline record checker and synthetic examples. Exercise logical deduplication, revision conflicts, evidence mismatch, prerequisite errors, and the limited stop/resumption rules the record model can express. Do not describe it as authentication, distributed exclusion, sandboxing, or remote-stop enforcement.
6. Generalize the existing research checker to discover experiment records and validate lifecycle/result shape. Permit completed exploratory and negative/inconclusive work. Do not require a particular Rust crate or the first hypothesis/experiment forever.
7. Defer an automated GitHub writer until its exact live owner type, capabilities, permissions, schema, and workflows are verified and a bounded adapter contract is exercised. Document transport and resource-enforcement conformance tests separately from offline record tests.

## Alternatives and reasons

**Comments as the canonical journal:** convenient, but update/delete semantics and shared-account attribution require additional preservation and authority checks. Versioned accepted records are easier to inspect alongside the affected research artifacts.

**A distributed database, scheduler, lease service, and custom UI now:** these could eventually solve measured coordination problems, but no observed workload currently establishes their necessity. A database transaction would also not atomically control a GitHub mutation, a provider request, and a remote worker's external effects.

**Documentation only:** leaves the known checker defect and record consistency errors unexercised. A bounded deterministic checker is a small testable instrument without a production service commitment.

**Freeze the current workflow and schemas permanently:** conflicts with the owner's research-driven direction. Versions protect specific records and comparisons; prospective migrations can change the protocol.

## Consequences and revision triggers

The baseline is cooperative. Record hashes detect content correspondence; reviewer metadata does not prove trusted authorship. A single integrator avoids conflicting accepted updates by procedure, and checker conflict detection is not a server lock. Raw artifacts and referenced commits require retention. Empty/missing source observations remain unknown until reconciled.

A GitHub outage can delay projection without changing accepted scientific content. High manual update cost, unacceptable staleness, demonstrated multiwriter conflicts, or a need for exclusive shared-resource execution can justify the smallest relevant automation. Any such revision must retain raw observations, define its failure model, and independently test the new guarantees.

See [coordination contract](../coordination.md), [primary-source review](../research/github-coordination-review.md), and [bounded adoption record](../coordination-adoption.md).
