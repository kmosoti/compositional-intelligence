# EXP-0002: Reusable abstraction and causal transfer

**Status:** planned; not preregistered; not implemented or executed. **Hypothesis:** [HYP-0002](../../research/HYP-0002.md). **Record:** [manifest](manifest.json).

## Scientific target and scope

Test whether a representation acquired from permitted experience supports transfer and selective causal control under bounded resources. The tested system boundary includes the controller, model, tools, learned artifacts, and runtime. Any claim about internal neural representations requires an instrumentable-model study; an external memory intervention establishes only the role of that external mechanism.

The current repository is a provisional instrument. A program, graph, neural representation, probabilistic model, or simpler algorithm can be selected on development evidence. No candidate must fit existing crate boundaries. Protocol versions constrain interpretation of particular runs; they do not freeze the future research direction.

## Proposed task distribution and splits

Develop a reproducible simulator with concealed rules, intervention tools, and independently checkable postconditions. Use an acquisition split, a development split, and evaluator-controlled holdouts. The proposed pilot has 24 held-out tasks: eight unfamiliar recombinations, eight label/domain transfers, and eight held-out causal structures. Sample more than one instance-generating structure within each stratum and record clustering explicitly. Freeze exact structure membership, seeds, and hashes before evaluation.

Random labels reduce surface shortcuts but do not prove absence of related pretraining knowledge. Record training-data uncertainty. Hold out structural rules and combinations, not just random seeds. Do not give the candidate a ground-truth graph unavailable to the baseline. The optional oracle arm is explicitly privileged and cannot establish a fair performance advantage.

## Arms and run matrix

| Arm | Mechanism | Proposed runs |
|---|---|---:|
| A | Competitive model, retrieval, deterministic tools | 24 tasks × 2 sampling seeds = 48 |
| B | A plus an acquired representation and its use mechanism | 48 |
| C | B's permitted information in a declared alternate serialization, with matched access | 48 |
| D | Simple deterministic solver with the same observation/intervention affordances | 24 |
| O | Oracle representation diagnostic; privileged information labeled | 24 |
| N | Relevant-relation and irrelevant-relation interventions on eight frozen tasks, two sampling seeds each | 32 |

Maximum: 224 runs. A, B, C, and D receive equal raw acquisition evidence and equal acquisition-budget opportunities, as well as matched holdout observation and intervention affordances. Record their actual acquisition expenditure; an algorithm may use less than its allowance. A, B, and C share task worlds, sampling-seed identifiers, intervention budgets, and initial observations. Same seed identifiers do not guarantee identical provider randomness; document provider behavior. Randomize run order and reset environment and task-private memory between arms. Each held-out task begins from the same frozen post-acquisition state; no facts or skills learned on one holdout may enter another holdout's starting state.

C receives a conversion of B's acquired content at a frozen point in the information timeline. Preserve its provenance, evidence cutoff, and availability time, and exclude later observations. Charge the acquisition that produced this content and the conversion to C's ledger; do not treat B's learning as free privileged information. Freeze the conversion and account for serialization-length mismatches. Candidate acquisition occurs only on permitted acquisition data.

N changes a relation predicted to control one decision and separately changes a task-irrelevant relation. Preserve formatting and size where possible. A selective change is stronger evidence than general degradation caused by malformed input. Include both informative and misleading correlation conditions in task generation.

## Measurements and analysis

Primary: paired difference in independently accepted task success, B minus A, under the fixed caps. Report each task and stratum; average stochastic repetitions within a task before paired uncertainty estimates. Use the frozen task-cluster definition for resampling and report the small pilot's limited precision. Do not treat repeated samples of one task as independent tasks.

Secondary: interventional prediction accuracy, observations needed to reach a frozen criterion, costs, latency, memory, and selective intervention effects. Report A/B/C/D on performance–cost plots; show O separately. Acquisition, inference, storage, and tool costs remain separate. If energy is not directly measured, record it as unknown and name the proxy; token counts, utilization, and dollars are not joules.

## Resource and stopping policy

Proposed per-run caps are 180 seconds, two CPU threads, 16 GiB host memory, 4 GiB GPU memory, 24 tool calls, 32,768 cumulative model input tokens, and 2,048 cumulative model output tokens. Model loading and acquisition costs must also be logged; they may not disappear outside the ledger. Proposed aggregate caps are 12 elapsed hours, 7,340,032 input tokens, 458,752 output tokens, and zero paid spend. The zero-spend plan permits only available local execution; paid/API execution needs a new authorized budget before freezing.

Stop after the frozen matrix, not when a desired effect appears. Treat task timeouts and task-caused tool failures as outcomes. If an independently established evaluator/infrastructure fault invalidates a block, retain the original block and rerun every paired arm with an explicit amendment record. If the aggregate cap prevents completion, publish an incomplete pilot; do not selectively drop difficult tasks or silently extend resources.

## Freeze gate and falsifiers

Before `pre_registered` can become true, fix the generator, task-family split, seeds, implementations, model versions, hardware limits, acquisition evidence and budget parity, conversion provenance and timing, intervention semantics, cost accounting, evaluator boundary, and executable analysis. Verify isolation of answer keys and holdout materials from workers. Exploratory pilots and development runs may proceed under existing scoped authorization with honest exploratory labels and preserved evidence. This document grants no additional paid, network, deployment, or human-session authority.

The tested candidate loses support if its benefit disappears with equivalent information and resources, depends on the oracle state, fails transfer outside familiar surfaces, or lacks the predicted selective intervention effect. A positive pilot motivates a new independent confirmatory protocol. It does not establish general intelligence, consciousness, or superintelligence.
