# EXP-0004: Assistance and retained human competence

**Status:** planned; not preregistered; no sessions scheduled or conducted. **Hypothesis:** [HYP-0004](../../research/HYP-0004.md). **Record:** [manifest](manifest.json).

## Learner, objective, and boundary

The initial exploratory learner is one human researcher. The question is whether assistance improves later independent programming ability as well as immediate output. A useful tool can increase assisted productivity without increasing unaided skill; both outcomes must remain visible.

Retention is measured behaviorally on new problems after assistance is withdrawn. Human memory is not directly inspected. During assessment, AI, acquisition-session answers, notes, generated code, and external search are unavailable. The same editor, compiler, and frozen local test interface remain available to every condition. Therefore “unaided” here means no cognitive assistance beyond those declared common tools, not absence of all technology.

The experiment does not identify competence loss with brain damage, establish the irreversibility of skill change, or assume that a tool is inherently competitive. A proposed machine analogue must separately identify the learning locus and which state survives withdrawal: model weights, prompts, episodic memory, executable skills, or the full composite. It is not part of this human pilot.

## Conditions and task construction

Use three conditions:

1. **Delegation:** the assistant supplies a solution and explanation; the learner may inspect them within the fixed session.
2. **Reconstruction:** the learner predicts an outcome or proposes a mechanism before feedback, reconstructs a solution, and verifies it with the permitted tools.
3. **Reference practice:** the learner works with a frozen documentation/example pack and the same editor/compiler, without generative assistance.

Choose a bounded programming domain, such as Rust state transitions or debugging, after a prior-skill assessment. Build 12 acquisition sessions in four matched blocks of three task families, one family per condition in each block. Randomize family-to-condition assignment within every matched block, then randomize and counterbalance condition order before acquisition. Match task difficulty using an independent rubric or pilot evidence, not post hoc success. Avoid assigning the same problem to multiple conditions.

Each acquisition task has different immediate and delayed assessment items. Delayed items require transfer to a new surface or composition and cannot be solved by copying a memorized answer alone. Keep answer keys and assessment items inaccessible to the acquisition assistant and learner. Freeze whether immediate assessment supplies correctness feedback, which feedback it supplies, and when. The proposed default withholds additional assistant or assessor answers, hints, and corrective feedback until that family's delayed assessment is complete; outputs from the identical permitted compiler/test interface remain available and are logged. Assessment practice itself may affect retention and must be recorded. Generic pretraining overlap remains an uncertainty; novel items and task separation reduce exact-answer contamination without proving its absence.

Learning carries across time. Counterbalancing cannot erase this. Before acquisition, freeze the schedule of subsequent learning sessions relative to every delayed assessment, including any overlap across related task families. Record immediate assessments, later sessions, outside practice, feedback, and other exposure as intervention history; they are not an empty delay. Analyze order and overlap effects as exploratory. The design is a personal pilot; population conclusions require a separately powered randomized study. A clean within-person reversal should not be claimed because learned skills cannot simply be washed out.

## Schedule, sample size, and resources

Proposed fixed sample: one participant, 12 acquisition sessions, four per condition. Each acquisition session lasts 25 minutes, followed by a ten-minute immediate unaided assessment. A separate ten-minute unaided transfer assessment occurs seven days later, with a predeclared tolerance of one day. Total planned participant time is 540 minutes. Final calendar dates require participant agreement before freeze; this document creates no automation or invitation.

For assisted acquisition, cap input at 32,768 cumulative tokens and output at 4,096 tokens per session using the same assistant/model version. Time is matched; actual assistance, reading, generation, and active reconstruction time are measured rather than assumed identical. Zero new paid spend is proposed. If execution requires paid access or a materially different resource plan, amend the budget before preregistration. Record model latency as part of assisted time.

Stop after the 12 sessions and their assessments. Do not stop because a condition appears better. Preserve timeouts and incomplete answers. Record missed delays and extra practice as deviations; do not silently replace inconvenient sessions. Freeze the missing-data analysis before starting, including whether delayed items outside the window are reported descriptively only.

## Outcomes and interpretation

Primary outcome: delayed transfer correctness, scored by frozen executable checks and a blinded rubric where tests alone are insufficient. Compare reconstruction with delegation first; reference practice is the second planned comparator. Report raw per-session and per-block outcomes. Twelve sessions do not justify a precise population effect or a strong null claim.

Secondary outcomes: acquisition correctness and completion time, immediate unaided performance, mechanism explanation on new cases, calibration against scored answers, and assistance exposure. Keep assessors blind to condition where feasible and record any unblinding. Subjective feeling of learning is secondary to independent performance.

The hypothesis loses support if reconstruction provides no retained benefit, ordinary reference practice matches it at lower cost, or apparent benefit is explained by unequal time, prior skill, or extra exposure. A tradeoff between immediate speed and retained skill is a substantive result; do not collapse it into an arbitrary single score.

Krakauer's proposed hysteresis requires more than a withdrawal decrement. Testing that claim needs a distinct protocol comparing learning histories at identical final access, against simpler practice/forgetting alternatives and sufficient longitudinal observation. This pilot measures complementarity for the specified learner and tasks; it does not test population tipping points.

## Freeze gate and future revision

Before preregistration, fix participant agreement and schedule, task matching, randomized family-to-condition assignment, condition order, overlap between learning and delayed assessments, immediate-feedback policy, permitted tools, assessment separation, scoring, assistant version, budgets, missing-data rules, and analysis. Confirm that no assessment answer key is exposed during acquisition. Architecture and learning policy remain revisable instruments. Preserve every frozen version and result; let evidence change subsequent hypotheses and implementation.
