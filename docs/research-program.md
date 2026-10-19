# Research program: intelligence through scientific and engineering investigation

**Status:** Active research direction; experiments remain planned. No new cognitive capability or experimental benefit is reported here.

**Updated:** 2026-10-19.

## Goal

Discover which mechanisms and combinations acquire useful representations, transfer to unfamiliar situations, retain what they learn, and act reliably under bounded resources. Build experimental instruments that let those questions be answered, and revise the instruments and questions as evidence accumulates.

The project's technical direction is governed by **research → experiments → analysis → renewed research**. Current code describes an instrument under investigation. It is not an oracle for architecture or intelligence. Entire decompositions may be replaced when a better hypothesis, counterexample, or experiment warrants it. [ADR 0002](adr/0002-research-governs-implementation.md) records this governance choice.

## Two connected lines of inquiry

The [Krakauer review](research/krakauer-intelligence.md) examines competing accounts of intelligence, understanding, efficient abstraction, conscious access, and tool-mediated learning. The [DeepSeek/Pi/Codex review](research/agent-harness-review.md) examines real execution machinery: selected context, service composition, tool languages, authority, concurrency, durable state, and recovery.

These contribute different evidence. A source walkthrough can establish how a runtime handles cancellation. It cannot establish that the runtime learns abstractions. A theory of cognition can motivate a memory mechanism. It cannot establish that the mechanism survives a crash or improves task success. The experimental program connects these claims while keeping their evidential requirements distinct.

## What is being evaluated?

Every protocol declares its unit of evaluation before scores are interpreted.

| Unit | Example question | Attribution limit |
| --- | --- | --- |
| Frozen learned model | What can this checkpoint infer from a specified input? | API-only access cannot identify hidden neural mechanisms |
| Controller or memory mechanism | Does structured state or learned escalation improve decisions? | Better context use does not establish a model-weight update |
| Model, harness, and tools together | Can the complete system achieve a goal with bounded cost? | A solver's contribution cannot silently become a capability of the base model |
| Human with the system | Does assistance improve current work and later unaided competence? | One person's exploratory result cannot establish population-wide effects |

Changing the boundary changes the claim. A system-level improvement is useful even if it does not reside inside the model. A claim about retained learning, however, must name what state changed and remains available at evaluation.

## Operational dimensions

These are measurement targets rather than a final theory of intelligence.

| Dimension | Observable question | Stronger claim that needs extra evidence |
| --- | --- | --- |
| Capability | Can the system meet independently checked postconditions? | General competence across unspecified environments |
| Efficiency | What quality is achieved for acquisition and execution resources? | A universal intelligence ranking from one efficiency ratio |
| Abstraction | Does a reusable representation support prediction and intervention? | A readable graph necessarily explains hidden neural computation |
| Transfer | Does performance survive new rules, structures, or recombinations? | An unseen instance necessarily lies outside pretraining experience |
| Adaptation | What retained state changes future performance? | Merely persisting a transcript is useful learning |
| Metacognition | Does an uncertainty estimate predict errors and improve decisions? | A plausible explanation faithfully reports internal reasoning |
| Information access | Which components can use which evidence, and when? | Shared access implies phenomenal consciousness |
| Reliability | Can effects be bounded, observed, and recovered? | Robust orchestration by itself demonstrates intelligence |
| Human complementarity | What useful competence remains after assistance is withdrawn? | All assistance necessarily helps or harms its user |

Fast/slow processing, verbal/nonverbal representation, local/shared information, and object-level/meta-level control are independent design axes. A background worker can be slow. A compact symbolic computation can be fast. Neither fact settles consciousness. Functional experiments will use those concrete names rather than a permanent conscious/subconscious software hierarchy.

## Research tracks and current experiments

| Track | Question | Current record |
| --- | --- | --- |
| Baseline and marginal utility | Does an added mechanism justify its end-to-end cost? | [HYP-0001](../research/HYP-0001.md), [EXP-0001](../experiments/EXP-0001/manifest.json), preserved as originally planned |
| Reusable abstraction | Does a representation causally support unfamiliar prediction and planning? | [HYP-0002](../research/HYP-0002.md), [EXP-0002](../experiments/EXP-0002/protocol.md) |
| Functional coordination | When do selective sharing and explicit checking improve quality/cost? | [HYP-0003](../research/HYP-0003.md), [EXP-0003](../experiments/EXP-0003/protocol.md) |
| Retained competence | Does assistance leave the learner more capable after withdrawal? | [HYP-0004](../research/HYP-0004.md), [EXP-0004](../experiments/EXP-0004/protocol.md) |
| Experimental infrastructure | Which request, effect, recovery, and evaluator boundaries are required? | [Harness review](research/agent-harness-review.md) and [engineering contract](agent-harness.md); mechanisms remain candidates |

These IDs identify plans, not executed studies or a fixed implementation sequence. EXP-0001 establishes an initial retrieval comparison. EXP-0002 is the first proposed bridge from the intelligence literature to mechanism-level tests. Pilot feasibility and expected information value determine which work proceeds next.

## From concept to a discriminating experiment

For the abstraction track, the concept is that reusable structure makes unfamiliar problems easier. The principle is transfer through a representation that does causal work. The invariant is that a claimed gain must not depend on privileged access to hidden answers or extra uncounted resources.

A possible mechanism is a learned relational state updated from observations and interventions. A small generated environment can expose causal rules, distractor correlations, and changed dynamics through controlled interfaces. The candidate must predict outcomes and choose actions. Equivalent-information text, retrieval, simple deterministic methods, and oracle information are separate controls. Intervening on the proposed representation tests whether it actually explains a specific behavioral change.

This is a proposal, not a requirement to build a graph or a new crate. If an ordinary small model or a compact classical method solves the problem at a better quality/cost point, retain that finding and replace the more complicated candidate. If the task cannot distinguish mechanisms, revise the task rather than manufacture an architectural victory.

## Accounting and comparison

Report a quality/resource profile rather than one supposedly universal intelligence score. Measure task success and transfer alongside acquisition exposure, inference and tool calls, elapsed time, retained storage, host/device memory, and energy when actually measurable. State which preparation and training costs are unavailable or excluded; amortize them only over an explicit workload.

Token counts, dollars, CPU time, and joules are different quantities. A provider's billing price is not an energy measurement. A faster implementation may consume more memory; a more accurate one may use more inference. Record the trade-off and the workload for which it matters.

When contrasting full harnesses, distinguish a native configuration comparison from a controlled mechanism comparison. Native providers can differ in protocols, models, tools, defaults, and permission boundaries. A claim about one component needs a design that isolates it. A multi-agent treatment needs equal-budget single-controller and independent-candidate controls.

## What would change the direction?

- Consistent transfer through compact, causally used representations would support the abstraction program, whether those representations are neural, symbolic, or distributed.
- Equal performance from an equivalent-information simple representation would weaken the case for a more elaborate memory architecture.
- Gains that disappear under matched resources would reclassify the result as a resource-allocation effect.
- A rigid pipeline beating adaptive coordination would favor the pipeline for that workload.
- Strong unaided transfer after assistance would challenge a local dependence hypothesis; reduced retained competence would challenge an assistance policy despite improved immediate output.
- Failure of a simulator, scorer, or recovery mechanism would trigger instrument repair and reruns, with the invalidated evidence preserved and labeled.

No finite task battery establishes general superiority over every possible intelligence. Any future superhuman claim must specify tasks, comparison population, resources, prior experience, and transfer requirements. The present work investigates these dimensions and does not report superintelligence or subjective experience.

## Records and next decisions

Keep literature claims with provenance and scope; implementation snapshots with commits; hypotheses with competing explanations; protocols with freeze status; and results with raw evidence and limitations. Record decisions that replace code as carefully as decisions that add it.

Before a confirmatory run, resolve every manifest's blocking choices: implementation identities, task generator and evaluator versions, data splits and access controls, seeds, resource caps, sample-size rationale, meaningful effect size, exclusions, and stopping rule. Planned documents do not satisfy that gate by existing. Exploratory pilots can resolve feasibility while remaining explicitly exploratory.

The smallest useful next implementation is the environment/evaluator boundary for a narrow transfer task plus simple controls and a minimal evidence log. The detailed choices remain subject to the protocol's freeze gate. A large permanent cognitive hierarchy should earn its existence from results obtained with these smaller instruments.
