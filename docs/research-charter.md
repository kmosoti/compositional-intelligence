# Research charter

**Stage:** research infrastructure and candidate design. No system capability or performance benefit demonstrated.

## Aim

Discover which mechanisms and compositions acquire useful representations, generalize to unfamiliar problems, preserve evidence, adapt through experience, and act reliably within bounded resources. Evaluate the complete system and, where explicitly studied, what its human user retains from working with it.

## First instrument

Build one persistent LLM-assisted agent for bounded software engineering and research tasks. Existing native harnesses provide an initial generation and tool-use capability. External task state, evidence, exact operations, and independent acceptance make that capability inspectable and testable. The first baseline is the same native harness under comparable conditions, not an intentionally disadvantaged competitor.

This is an implementation priority, not a theory that intelligence requires LLMs. Neural, symbolic, probabilistic, graph, dynamical, developmental, and collective approaches remain candidates. [ADR 0004](adr/0004-llm-assisted-research-instrument.md) records the change of starting point.

## Direction follows investigation

Research, experiments, critical analysis, and renewed research determine technical direction. Current source and prior art are revisable information. Theories, including Krakauer's, motivate competing explanations and discriminating tests rather than mandatory conclusions.

Freeze individual comparisons, not the project's architecture. Preserve earlier protocols, unsuccessful attempts, and negative findings. Exploratory implementations need a clear question, not already-positive results. User goals, permissions, resource limits, evidence integrity, and independent acceptance constrain the work. [ADR 0002](adr/0002-research-governs-implementation.md) remains in force.

## Resources and attribution

The local host profile previously recorded was an i7-10750H, 32 GB RAM, and RTX 3060 Laptop GPU with 6 GB VRAM. Verify actual hardware per run; do not extrapolate accelerator benchmarks to it. Hosted-model work is a separate declared resource boundary. The laptop does not pay the provider's hidden compute cost, and subscription access does not authorize API billing.

Rust is the current runtime starting point, not a scientific requirement. Favor explicit behavioral interfaces and measured suitability. No mandatory graph server, vector service, distributed swarm, or new model training is required for the initial instrument.

## Epistemic boundaries

Distinguish observations, source assertions, hypotheses, predictions, derivations, and unknowns. Distinguish capability, efficiency, abstraction, transfer, retained learning, metacognition, information access, and subjective experience. Efficient execution does not establish general intelligence; persisting a transcript does not establish useful learning; reduced tokens do not establish preserved quality.

Compare quality/resource profiles, including preparation, failures, retrieval, verification, maintenance, and unavailable measurements. Favor fresh-task and long-lived-session comparisons rather than silently using one to make claims about the other.

## Non-goals of the first slice

Reproducing frontier models, emulating a brain, mandatory hypervectors, optimizing token counts at the expense of outcomes, automatic architectural self-deployment, or unbounded delegation. These are scope choices, not impossibility claims. The [research program](research-program.md) keeps alternatives visible.
