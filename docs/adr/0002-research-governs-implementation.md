# ADR 0002: Research governs direction; implementation remains replaceable

**Status:** Accepted as project governance, not as an empirical finding.

**Date:** 2026-10-19.

**Basis:** The project owner's explicit direction that research and experiments govern the project and that the current code is not an oracle.

## Context

A research repository can accidentally turn an early implementation into a theory. Crate boundaries become presumed cognitive modules, a convenient benchmark becomes the definition of intelligence, and future proposals are judged by compatibility with yesterday's code. This is path dependence, not evidence that the design is correct.

The project combines scientific investigation with the engineering of experimental instruments. It must permit both to evolve, including large changes of architecture, without losing the ability to interpret earlier observations.

## Decision

Research, controlled experiments, critical analysis, and renewed research govern technical direction. Code, diagrams, language choices, role names, interfaces, and baselines are revisable artifacts. Their existence gives them no privileged scientific status. A supported contradiction, a decisive counterexample, or an infeasible cost can justify replacing a design without preserving its abstraction boundaries.

The governing distinctions are:

| Item | What it establishes | What can change |
| --- | --- | --- |
| User goal, permission, and resource envelope | The authorized purpose and constraints | Through the applicable user decision; a research hypothesis grants no new authority |
| Literature or mathematical argument | A claim with assumptions and evidence | Interpretation and applicability as counterevidence appears |
| Current code | One implementation state and its observed behavior | Any part of the active implementation, within authorized scope |
| Frozen experiment protocol | The meaning of a specific comparison | Prospectively through a recorded amendment or successor experiment |
| Tests and acceptance criteria | Operational checks for specified properties | Through justified amendments, retaining the original outcomes |
| Experimental record | What was actually done and observed | Corrections are appended with provenance; inconvenient evidence is retained |

Before a material change of direction, record the discriminating question, the strongest simpler alternative, the assumptions carrying the decision, and the smallest informative test or derivation. Separate exploratory findings from confirmatory tests. Reopen a settled choice when new evidence has decision value, rather than maintaining either permanent churn or permanent architectural loyalty.

Exploratory code can be written to obtain evidence that does not yet exist. A candidate needs a meaningful question and proportionate rationale, not a favorable result before it may be built. Scientific adoption is a later decision.

## Scientific freedom and experimental integrity

Freeze the protocol, evaluator, and relevant versions for a run. This protects interpretation; it does not freeze the project. If a test measures the wrong property, preserve the old run, document the defect, and evaluate under a revised protocol. Do not redefine a result after seeing it and present the revised definition as preregistered.

Theory can reject an impossible candidate before implementation. Engineering failures can invalidate an instrument without refuting its scientific hypothesis. A scientifically unhelpful implementation can pass every software test. Record which of these happened.

## Consequences

Rapid architectural replacement is permitted when justified. Old code can leave the active tree while remaining available in version history. Negative results and superseded hypotheses remain part of the research record. Rust, a small-model baseline, signal-driven control, and heterogeneous composition are current starting choices or candidates; each must earn its role for the relevant question.

Krakauer's research and competing accounts inform the questions. The project does not exist to confirm an author's position, deny all LLM intelligence, or validate a preselected path to superintelligence. Its useful outputs include new mechanisms, measured limits, rejected hypotheses, and better problem representations.
