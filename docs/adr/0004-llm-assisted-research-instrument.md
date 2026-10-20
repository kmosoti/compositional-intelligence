# ADR 0004: Begin with an LLM-assisted research instrument

**Date:** 2026-10-20. **Status:** owner-requested direction rewrite submitted for review; implementation and scientific adoption remain unestablished.

## Task and authority

The owner requested rewriting the repository approach around the LLM-assisted agent design and evaluating lessons from the linked HELIX Reddit post. Scope: project direction, candidate architecture, runtime/context contracts, instructions, and a new draft experiment. Base snapshot: `9252797e75e20ca83af1bbfde7d291fc35cb6499`.

Mutable artifacts are the documents and new planning records in this change. Existing Rust/runtime code, tests, CI, frozen evaluation material, coordination schemas/records, and EXP-0001 through EXP-0004 remain unchanged. No inference spending, installation, deployment, account settings, or live Wiki publication is included. One author submits this branch; authorship is not independent acceptance.

## Problem and counterexample

The previous first comparator emphasized a local quantized small model. The agreed near-term objective now uses existing LLM harnesses to build a useful research instrument. Leaving the old starting point in the primary documents would send implementation toward a different resource/access boundary.

HELIX supplies a second concrete counterexample: a large reported reduction in known tokens coexists with fewer reported solves and more requests/output. Token reduction alone is therefore an inadequate adoption gate. Exact retention also does not prove that the agent can discover the evidence needed for a later decision.

## Decision

Prioritize one persistent agent with external task/evidence state, one native worker, deterministic execution boundaries, and protected acceptance. First compare the same pinned native harness with and without recoverable context projections and preauthorized mechanical flow. Next investigate graph memory and executable procedures; vectors, reviewers, additional providers, and other mechanisms remain independently justified extensions.

Use Rust and local records as initial engineering choices. Do not build a permanent LLM manager, mandatory agent hierarchy, graph/vector server, or distributed swarm before a discriminating experiment requires it.

## Evidence and alternatives

The [HELIX review](../research/helix-context-review.md) separates inspected code, reported outcomes, arithmetic, and unresolved claims. It motivates hypotheses, not product adoption. The [architecture](../architecture.md) derives from the owner-approved design discussion; its cognitive benefits remain hypotheses.

Alternatives remain live: use a native harness unchanged; pursue a local small-model baseline; use direct feedback/dynamical control; construct better tools/environments; or investigate developmental/collective mechanisms. A native baseline with fewer moving parts is preferable where additions fail matched comparisons.

## Compatibility and migration

This supersedes the immediate implementation priority in earlier overview documents, not their historical hypotheses or results. Preserve earlier experiment protocols and the research-governance and coordination decisions. No existing runtime interface is changed by this documentation amendment. Public API/schema changes require separate implementation review.

Maintain one canonical source for each contract and link vendor instructions to it. Wiki source updates are separate from publishing the live Wiki. Do not label this change an alpha release or an implemented agent.

## Discriminator and acceptance

The smallest useful test is a fake-adapter, exact-candidate, restart-safe task instrument, followed by an explicitly authorized context/tool-flow pilot. [EXP-0005](../../experiments/EXP-0005/protocol.md) freezes neither a numerical savings target nor model entitlement; execution is blocked until its unresolved protocol choices and budgets are settled.

Document acceptance requires coherent links, preservation of existing scope and authority, explicit implementation status, accurate source attribution and arithmetic, and an honest validation report. Independent review and integration are separate from submission. A later positive cognitive claim requires held-out comparisons, quality gates, complete-enough accounting, and uncertainty analysis.

## Risks and rollback

Risks include hidden native context behavior, missing usage, harmful evidence projection, retrieval overhead, stale skills, and accidental authority expansion. Keep full-evidence/native controls, feature-level disable paths, and artifact history. Reject or narrow mechanisms whose quality-cost gains fail to survive realistic shifts. Revise this direction when better evidence or a cheaper informative experiment warrants it.
