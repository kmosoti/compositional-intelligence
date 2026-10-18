# Research charter

**Stage:** research infrastructure only. No system capability, general intelligence, or performance benefit demonstrated.

## Aim
Test whether a small set of complementary computational mechanisms generalizes to unfamiliar problems at lower total cost than a strong small-model baseline.

## Boundaries
Initial target is a 6 GB RTX 3060 laptop GPU, 32 GB host RAM and six-core Intel CPU. Never extrapolate published H100 benchmarks to this hardware without local measurements. Rust-first runtime; verified native libraries allowed.

## Finite means
Compositional generativity is a **research target**. Combinatorial recombination is not evidence of meaningful reasoning or transfer. Measure in held-out recombinations with explicit semantic validity tests.

## Epistemic rules
Observations, derived claims, unsupported hypotheses and counterfactual predictions have distinct types and provenance. Negative findings are publishable. Claims of causality require intervention or a justified identification design.

## Non-goals
Reproducing frontier models from scratch, arbitrary mandatory brain regions, million-token local neural context, self-modifying deployment and optimizing isolated token/s numbers at the expense of end-to-end task outcomes.
