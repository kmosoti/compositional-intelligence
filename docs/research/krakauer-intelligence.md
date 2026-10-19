# Krakauer, intelligence, and the experiments that matter

**Reviewed:** 19 October 2026. **Status:** literature appraisal and proposed research; no project experiment reported here has been run.

This review extends the [agent-harness research](./agent-harness-review.md) and informs the [research program](../research-program.md). Research questions, competing explanations, and experiments govern the project's direction. Existing code is a revisable instrument: its behavior is not an oracle for intelligence, and its architecture, language, or entire implementation may be replaced when a better experiment requires it. Krakauer's theories receive the same scrutiny.

## Best current interpretation

David C. Krakauer challenges the inference from impressive performance to intelligence. The useful question is whether a system acquires economical, reusable ways to solve unfamiliar problems. His interviews express strong skepticism about LLM intelligence, but his published research is more qualified. The 2023 perspective entertains distinct kinds of understanding; the emergence paper regards emergent intelligence in LLMs as unproven under its proposed criteria; his 2026 generality preprint explicitly recognizes statistical general intelligence. [K1], [K3], [K4], [K5]

These are distinguishable claims, not a settled verdict that LLMs have no intelligence under every definition. The project should test operational properties rather than defend a label. It must remain possible for a single neural model, deterministic solver, conventional harness, or unfamiliar architecture to outperform the preferred composite.

## Primary-source ledger

| Source | Status, date, and relevant claim | Evidential limit |
|---|---|---|
| [K1: The Generalist interview][K1] | 23 September 2025. Publisher chapters cover his argument against LLM intelligence, inference/representation/strategy, tool dependence, and unconscious creativity. | Interview judgment. Publisher description and chapter anchors were inspected; a complete primary transcript was not retrieved. |
| [K2: StarTalk, *What Is Intelligence?*][K2] | [Episode metadata][K2date] dates the podcast to 2 October 2026. Official description covers intelligence, consciousness, unconscious problem solving, and superintelligence. | Establishes topics, not exact spoken wording. No invented transcript or quotations from unofficial summaries. |
| [K3: Mitchell and Krakauer, understanding][K3] | PNAS perspective, 2023. Surveys competing accounts and advocates investigating and integrating diverse cognition. | Conceptual synthesis, not a controlled comparison or proof of the limits of future systems. |
| [K4: Krakauer, Krakauer, and Mitchell, emergence][K4] | Preprint 10 June 2025; [journal publication][K4journal] 14 May 2026. Separates capabilities from intelligence and asks for causal abstractions, economical solutions, and transfer. | Proposed framework informed by prior research. A surprising score jump does not establish its mechanism. |
| [K5: *The Rise and Fall of G in AGI*][K5] | Preprint, 10 April 2026. Studies benchmark covariance and interprets changing factor structure as diversification. | Observational and preliminary; statistical factors do not identify their generating mechanisms. |
| [K6: *The Kekulé Problem*][K6] | Cormac McCarthy essay, introduced by Krakauer, 17 April 2017. Explores nonverbal insight and unconscious processing. | Speculative essay, not controlled neuroscience or a demonstrated software architecture. |
| [K7: *Competitive and Complementary Tools*][K7] | Preprint, 20 July 2026. Models retained competence and reliance as a coupled dynamical system. | Predictions depend on assumed learning/offloading dynamics; central feedback claims require longitudinal tests. |
| [K8: *Large-Language Models as a Cognitive Virus*][K8] | Coauthored preprint, 3 September 2026. Models possible population tipping toward dependence. | Conditional model, not observed universal collapse. The authors also allow beneficial integration. |

For K7, the author-listed preprint is canonical; its manuscript was inspected through an [accessible manuscript mirror][K7mirror]. Publication status does not determine whether a claim is correct. Dates constrain which systems an observation concerns.

## Claims, counterevidence, and unresolved alternatives

**Supported interpretation of K4:** internally useful abstractions and transfer deserve investigation. The paper acknowledges candidate representations and generalization evidence. It therefore cannot support the claim that sequence models literally have no internal representations. Nor does it prove that scaling can never produce economical reasoning. Efficiency is informative, but making it definitional is a theoretical choice. [K4]

**Counterevidence to unrestricted incapacity claims:** Nanda, Lee, and Wattenberg identify a linear board representation in an Othello sequence model and alter behavior through interventions on that representation. This supports meaningful internal structure in a controlled domain, not arbitrary world understanding. Lake and Baroni demonstrate systematic generalization through meta-learning on compositional tasks. That challenges a blanket impossibility claim about neural compositionality; the training distribution and task scope still matter. [R1], [R2]

**Qualification from K5:** its abstract states, “In strictly psychometric terms, AI models exhibit general intelligence suppressing specialized intelligences.” Its statistical sense of generality must remain distinct from a single general causal faculty. [K5]

**Our appraisal:** these are observational benchmark comparisons with structured missingness and small complete-case samples. Reported parallel analysis does not retain a second component. Shared ancestry and evaluation conditions complicate causal architectural interpretations. [K5]

**Our mathematical deduction:** removing a positive first principal component can itself induce negative residual correlations. With unit component vector `v` and scores `x`, residuals satisfy `r = (I − vvᵀ)x` and `vᵀr = 0`. Thus `Σj vj Cov(ri, rj) = 0`; a positive variance term requires some negative cross-covariances. Negative residuals alone do not establish computational trade-offs. Detailed patterns may remain informative, but need suitable null models and interventions.

## Conscious, nonconscious, and observable software functions

The user's conscious/subconscious distinction should widen the investigation without committing it to a brain metaphor. Three operational dimensions are useful:

| Dimension | Question | Candidate measurement |
|---|---|---|
| Local processing | What useful computation happens without being shared across the system? | Local prediction quality, cost, and contribution under ablation. |
| Information availability | Which evidence becomes accessible to other mechanisms when needed? | Correct cross-component use, stale decisions, useful information per byte. |
| Self-monitoring | Can the system estimate and use information about its own reliability? | Properly scored confidence and improved decisions under verification budgets. |

Dehaene, Lau, and Kouider's 2017 neuroscience review distinguishes nonconscious computation (C0), global availability (C1), and self-monitoring (C2), arguing that the latter two can dissociate. These are theory-informed functional distinctions, not a settled universal consciousness detector. [C1]

Butlin and colleagues' indicator approach evaluates systems relative to theories connecting computational properties with experience. The inference remains conditional on those theories and their application to artificial systems. Architectural checkboxes or first-person reports do not independently establish subjective experience. [C2]

**Our engineering translation:** fast/slow describes computation allocation; local/shared describes information topology; verbal/nonverbal describes representation; object/meta describes what is modeled. Keep these axes separate. An asynchronous worker is not thereby a subconscious mind. A distributed evidence-sharing protocol can test selective availability without requiring a permanent central router. Leases, versions, and authority still need explicit mechanisms.

The project can investigate these functions while leaving phenomenal consciousness unresolved. A successful coordination experiment would establish a performance result for its tested mechanism and workload, not a conscious machine.

## System boundaries change the conclusion

**Our analysis:** declare the unit being evaluated: frozen model, model plus harness, learning system over repeated tasks, or human plus tools. A harness may improve the composite without changing model weights. A retained skill may improve later behavior even when its implementation is external to the model. These are different learning claims.

Likewise, record the acquisition budget, prior training, retrieval corpus, tool affordances, persistent state, and human preparation. An apparently economical solution may merely move costs outside the accounting boundary. Tokens, dollars, latency, and energy measure different things. Compare performance–resource curves when no candidate dominates across all relevant budgets.

Separate the frozen scientific protocol from candidate implementations. Replacing code should be easy; silently changing the question, hidden cases, or acceptance rule after seeing results would invalidate comparison. Preserve the old candidate and evidence, register any protocol amendment, then rerun an appropriate comparison. The research can move quickly without treating passing existing tests as proof that the current architecture is scientifically preferred.

## From review to falsifiable work

| Hypothesis | Minimal discriminating comparison | Evidence that weakens it |
|---|---|---|
| [HYP-0002: reusable abstraction and causal transfer](../../research/HYP-0002.md) | Compare simple controllers and candidate representations on generated worlds with held-out rules; selectively intervene on claimed abstractions. | Gains vanish on unfamiliar structures, survive removal of the alleged mechanism, or depend on unavailable oracle information. |
| [HYP-0003: functional coordination](../../research/HYP-0003.md) | Independently vary selective evidence sharing and uncertainty-triggered deliberation against matched-budget controls. | Development-frequency random or simpler fixed control provides the same reliability and cost. |
| [HYP-0004: retained human competence](../../research/HYP-0004.md) | Compare delegation, active reconstruction, and ordinary practice; test delayed unaided transfer. | Assistance improves immediate output but the proposed complementary mode yields no retained benefit. |

These hypotheses are independent. Better system performance can coexist with reduced human retention. Conversely, a teaching interaction can improve the researcher while slowing immediate production. K7 motivates this distinction; K8 adds a possible social-feedback mechanism. Neither settles the direction of every person's outcome. [K7], [K8]

**Smallest useful next study:** implement a disposable generated-world environment and two competitive controllers, then add one representation intervention. Predeclare splits, success checks, budgets, and exclusions. Retain failed runs and compare equivalent information access. This establishes whether the new mechanism earns further investigation before constructing a permanent hierarchy.

**What would change our conclusions:** robust transfer and selective causal interventions would strengthen abstraction claims; equal-budget simpler systems would weaken architectural complexity claims; delayed unaided gains would challenge local dependence predictions. Define any future superhuman claim by task distribution, comparison population, acquisition resources, and transfer requirements. No current repository result warrants that label.

## Additional primary sources

- [C1: Dehaene, Lau, and Kouider][C1], *What is consciousness, and could machines have it?* Science, 27 October 2017; institutional full text inspected.
- [C2: Butlin and colleagues][C2], *Identifying indicators of consciousness in AI systems*, online 10 November 2025, 2026 journal issue; publisher material and its [2023 detailed predecessor][C2pre] consulted. Theory-dependent assessment, not an experimentally calibrated consciousness test.
- [R1: Nanda, Lee, and Wattenberg][R1], *Emergent Linear Representations in World Models of Self-Supervised Sequence Models*, BlackboxNLP, December 2023; publisher findings inspected.
- [R2: Lake and Baroni][R2], *Human-like systematic generalization through a meta-learning neural network*, Nature 623, 115–121, 2023; publisher findings and scope inspected.

[K1]: https://www.generalist.com/p/maintaining-human-intelligence-in-the-ai-era-david-krakauer
[K2]: https://startalkmedia.com/show/what-is-intelligence-with-david-krakauer/
[K2date]: https://podcasts.apple.com/sg/podcast/what-is-intelligence-with-david-krakauer/id325404506?i=1000791530524
[K3]: https://arxiv.org/html/2210.13966v3
[K4]: https://arxiv.org/html/2506.11135v1
[K4journal]: https://doi.org/10.1098/rsta.2025.0014
[K5]: https://arxiv.org/html/2604.09911v1
[K6]: https://nautil.us/the-kekul-problem-236574
[K7]: https://arxiv.org/abs/2607.18460
[K7mirror]: https://www.researchgate.net/publication/410697597_Competitive_and_Complementary_Tools
[K8]: https://arxiv.org/html/2609.03344v1
[C1]: https://escholarship.org/content/qt56b2q8h9/qt56b2q8h9.pdf
[C2]: https://doi.org/10.1016/j.tics.2025.10.011
[C2pre]: https://arxiv.org/abs/2308.08708
[R1]: https://aclanthology.org/2023.blackboxnlp-1.2/
[R2]: https://www.nature.com/articles/s41586-023-06668-3
