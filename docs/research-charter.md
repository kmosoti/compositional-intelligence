# Research charter

**Stage:** research infrastructure only. No system capability, general intelligence, or performance benefit demonstrated.

## Aim
Discover which computational mechanisms and compositions acquire useful representations, generalize to unfamiliar problems, preserve evidence, adapt through experience, and act reliably within stated resources. Test whether a small set of complementary mechanisms improves the quality/cost frontier over competitive alternatives. Evaluate both the artificial system and, where explicitly studied, what its human user learns from working with it.

## Direction follows investigation
Research, experiments, critical analysis, and renewed research determine the technical direction. Current source code and architecture are provisional instruments. They may be substantially replaced; implementation history is not scientific authority. Theories, including Krakauer's, contribute competing explanations and discriminating tests rather than mandatory conclusions.

Freeze the protocol of a particular comparison so it can be interpreted. Revise subsequent protocols, abstractions, and implementations when evidence warrants it, preserving earlier versions and negative findings. User goals, authorized scope, resources, and evidence integrity constrain the work. See [ADR 0002](adr/0002-research-governs-implementation.md).

## Combined science and engineering
The [research program](research-program.md) connects the [Krakauer literature review](research/krakauer-intelligence.md) with the [DeepSeek/Pi/Codex implementation review](research/agent-harness-review.md). Cognitive claims require appropriate transfer and mechanism evidence. Execution claims require appropriately scoped engineering evidence. Neither type substitutes for the other.

Distinguish capability, efficiency, abstraction, statistical generality, learned transfer, metacognitive control, conscious access, and phenomenal consciousness. Functional software experiments address selected dimensions; their outcomes do not automatically establish subjective experience or superintelligence.

## Boundaries
Initial target is a 6 GB RTX 3060 laptop GPU, 32 GB host RAM and six-core Intel CPU. Never extrapolate published H100 benchmarks to this hardware without local measurements. Rust is the current runtime starting point; language and backend choices remain revisable under measured requirements. A different hardware or hosted-service arm must declare its resource and access conditions rather than inherit local conclusions.

## Finite means
Compositional generativity is a **research target**. Combinatorial recombination is not evidence of meaningful reasoning or transfer. Measure in held-out recombinations with explicit semantic validity tests.

## Epistemic rules
Observations, derived claims, unsupported hypotheses and counterfactual predictions have distinct types and provenance. Negative findings are publishable. Claims of causality require intervention or a justified identification design.

## Non-goals
Reproducing frontier models from scratch, arbitrary mandatory brain regions, million-token local neural context, self-modifying deployment and optimizing isolated token/s numbers at the expense of end-to-end task outcomes.

These are current scope choices, not claims of impossibility. Changing scope requires an explicit rationale and the necessary user authorization; an attractive diagram or existing crate cannot decide it.
