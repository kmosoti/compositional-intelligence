# Agent Harnesses: Science, Engineering, and Composition

## DeepSeek Harness, Pi, and Codex

Source snapshot: 19 October 2026. Imported into the research program on the same date.

This is a dated implementation review. Its architectural judgments are revisable inputs to the [research program](../research-program.md), alongside the [Krakauer literature review](krakauer-intelligence.md). Current source is evidence about these implementations, not an oracle for the project's direction. No benchmark experiments were executed for this review.

## 1. The main finding

These projects are three overlapping approaches to building a stateful system that can act toward a goal using imperfect inference. The model proposes interpretations and actions. The surrounding software determines what information reaches it, which actions it can express, when actions may execute, what survives interruption, and what counts as a completed result. Useful capability belongs to this combined system.

My interpretation of their strongest architectural lessons is: DeepSeek makes the runtime itself extensively composable; Pi exposes separable model, controller, session, and tool layers, with a distinct durable runtime alongside the coding CLI; Codex integrates request consistency, execution policy, persistent state, and application lifecycles. These are emphases, not exclusive capabilities or measured rankings. DeepSeek also has carefully captured requests and execution policy. Pi also has recovery machinery. Codex also supports extension and composition.

The scientific question is therefore more precise than which harness is smartest: which decomposition makes a particular task observable, expressible, controllable, recoverable, and verifiable, within a specified resource budget? The engineering question is how those properties survive concurrency, changing configuration, unreliable services, lossy memory, and incorrect model proposals.

### Scope and pinned versions

| System | Inspected source | Commit time, UTC | Version interpretation |
| --- | --- | --- | --- |
| DeepSeek Harness | deepseek-ai/deepseek-harness, master, 687f282e8625c6b8d11ff58211a90524be2e4317 | 17 Oct 2026, 07:22:43 | Root and CLI manifests: 0.2.1-rc.2 |
| Pi | earendil-works/pi, main, d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03 | 19 Oct 2026, 09:35:34 | Coding agent, agent core, Durable: 1.3.0 |
| Codex | openai/codex, main, 4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857 | 19 Oct 2026, 14:08:49 | Main-branch snapshot; workspace version is a placeholder |

The historical badlogic/pi-mono address redirects to earendil-works/pi. DeepSeek Harness is the actual first-party harness, rather than an unofficial DeepSeek API wrapper. The review concerns the public harness implementations; proprietary model training, inference services, and hosted-service internals cannot be established from these repositories. These snapshots may include capabilities absent from an installed release or disabled in a particular configuration. [D0] [P0] [C0]

I traced critical production paths and read representative regression and property tests. I did not execute the complete applications, their test suites, or paid model benchmarks. This is a deep architectural source review of selected mechanisms, not an exhaustive security audit, proof of correctness, or empirical performance ranking. Claims marked as interpretation or proposal are deductions and recommendations rather than documented product guarantees.

## 2. What an agent harness actually does

A useful analytical decomposition has six steps. It admits a goal and constraints; builds the next model input from selected evidence; obtains a proposed action or answer; validates and authorizes an executable operation; records observations from execution; and decides whether to continue, stop, or ask for outside input. Real implementations overlap some steps and may add hooks, queues, tools, and model calls around them.

The model is not the entire policy of the system. A schema repair changes its proposed arguments. A sandbox changes which consequences are reachable. A context selector changes what it knows. A budget can terminate a promising search. A verifier can reject an attractive but incorrect answer. Each is a causal intervention in the resulting behavior.

One compact model is:

```text
x_t       = actual workspace, process, and external-service state
h_t       = recorded interaction and execution history
m_t       = reusable external memory
c_t       = Context(h_t, m_t, observations, constraints, budget)
proposal  = Model(c_t)
action    = Admit(proposal, schema, current authority, limits)
x_(t+1), observation = Execute(action, x_t)
decision  = Evaluate(goal, evidence, remaining budget)
```

This is an explanatory model, not a claim that these implementations solve a formal partially observable Markov decision process. They generally do not maintain calibrated belief distributions or known transition models. The lens is useful because the real state remains only partly observed. A command timing out, a stale file read, or an interrupted API response can leave several possible world states consistent with the transcript.

ReAct supplies a foundational example of interleaving actions and observations so later decisions can revise earlier ones. Its experiments do not establish that verbose reasoning text is always beneficial or that such text exposes the model's internal computation. The practical principle is feedback: acquire evidence capable of changing the next decision. [R1]

### The dimensions that matter

| Dimension | Question | Concrete mechanisms |
| --- | --- | --- |
| Representation | What can a proposal or observation express? | Message types, schemas, tool language, code actions |
| Observation | Which distinctions can the system detect? | Search, file inspection, tests, telemetry, provenance |
| Control | What causes another step or termination? | Queues, hooks, stop conditions, budgets, cancellation |
| Memory | What survives, and what is currently visible? | Logs, branch projections, summaries, retrieval, task checkpoints |
| Effects | What changes outside the model? | Filesystem operations, shell processes, remote API calls |
| Authority | Who can permit an effect? | Capabilities, approval policy, process confinement, network policy |
| Composition | How are parts connected and replaced? | Service dependencies, extension events, interpreters, SDK boundaries |
| Concurrency | Which operations may overlap? | Barriers, task ownership, ordered observations, resource limits |
| Verification | What establishes useful success? | Postconditions, independent checks, acceptance tests, external evidence |
| Adaptation | What changes between attempts? | Context, retained experience, skills, runtime code, model weights |
| Economics | What is consumed per accepted result? | Model calls, tokens, CPU/RAM, tools, latency, human attention |

There is no reason to expect one design to dominate every dimension. A more expressive action language may complicate confinement. More aggressive summarization saves context while risking lost distinctions. More workers can shorten independent searches while increasing conflicting mutations. The appropriate design is conditional on the task and the failure costs.

## 3. DeepSeek Harness: composing the runtime itself

### 3.1 The important abstraction is a graph of software capabilities

DeepSeek assembles model access, tools, sessions, the default loop, compaction, sandboxing, and delegation through Cordis plugins. Its base configuration is direct evidence of this composition: the product is assembled from separately mounted services and policy packages. A consumer depends on a service contract; a provider supplies an implementation. This is a software dependency graph, not a graph of learned neurons. [D1]

Cordis gives dependencies a lifecycle. A component can wait for required services, activate when they become available, and unload or reload when the relevant dependency implementation changes. The vendored fiber implementation checks dependency epochs to avoid continuing stale activation. Registrations and resources can belong to the component that created them. [D2]

The linked Cordis paper gives this a formal vocabulary: effects describe changes a component makes, while coeffects describe what it requires. Its context is a runtime environment for dependency and effect mediation, distinct from an LLM token window. Its composition results are conditional on the defined interfaces and reversible boundaries; they do not prove agent correctness or increasing intelligence. [R2]

### 3.2 Reversible component lifetime has a limited boundary

The source registers disposers for managed effects. Cleanup inside a grouped effect runs in reverse registration order, whereas independent top-level effects unload concurrently. Cleanup failures are logged and contained. It would be incorrect to describe the entire runtime as a globally sequential rollback transaction. The vendored-loader notes also acknowledge eager, nontransactional configuration mutations. [D2]

This mechanism can remove an event listener, unregister a tool, close an owned resource, or replace a provider. It does not undo an arbitrary external operation. If the tool already published a deployment or sent a message, removing its plugin cannot erase that consequence. The corresponding engineering obligation is to define which resources are owned, which changes have valid inverse operations, and which operations require compensation or reconciliation.

The benefit is easier replacement and lifecycle management. The cost moves into dependency identity, event ordering, activation failure, and cleanup correctness. A small stable agent does not automatically need this much dynamic composition; it becomes more valuable when the runtime itself must change while work remains active.

### 3.3 The request is derived from accepted history

The most consequential source path is agent-loop/src/agent.ts. At the model boundary, it logs the request configuration, derives the model-visible messages from the session, and freezes the resulting request. The model adapter separately binds effective settings and dispatch to one registration. This prevents a request from resolving against one provider instance and accidentally dispatching through a replacement midway. [D3] [D4]

This supports causal debugging: what tools, messages, and model settings did the harness actually present? It avoids treating UI text as the entire request. It does not make remote model behavior deterministic, capture hidden server-side processing, or snapshot the external workspace. The trustworthy boundary is the request representation under the harness's control.

### 3.4 Parallel execution and ordered evidence are different

The tool scheduler permits bounded parallel bodies, uses exclusive calls as barriers, and commits results in the model's call order. Calls are reclassified before starting, so earlier results or configuration changes can affect later execution. Cancellation stops new starts, drains started work, and records explicit outcomes for skipped calls. [D5]

Stable observation order makes transcripts more reproducible even when work finishes out of order. It cannot make conflicting physical mutations serializable. Correct concurrency classification is still required. A slow early call can also delay the recorded visibility of later results that have already completed.

The general lesson is to specify three orders separately: admission order, physical execution/completion order, and observation order. Treating them as a single sequence hides races and makes performance claims difficult to interpret.

### 3.5 Programmatic tool calling moves composition into ordinary code

DeepSeek's optional programmatic tool calling exposes the calling agent's visible tools to a small executable program. Nested calls pass through the policy pipeline and preserve initiating-agent identity. Native tool presentation remains the base profile default; this mode is a configurable capability. [D6] [D1]

The Node implementation uses a separate process, strips erasable TypeScript syntax, bounds execution and communication, clears the program-visible environment, and applies the selected filesystem confinement. Dynamic Node imports remain available. Syntax stripping is not type checking, and a V8 heap budget is not a total process-memory guarantee. [D7]

Its useful mechanism is straightforward: one model decision can express a loop, parallel reads, filtering, or a reduction, then ordinary computation performs those operations. Only selected results need enter the next model request. This can reduce round trips and irrelevant data traffic, but the benefit depends on the workload and the model's competence at writing such programs. Subcall provenance and partial-effect handling become more important because one visible model action can now contain many effects.

### 3.6 Persistence and sandboxing are precisely scoped

The checkpoint policy flushes the session before a model dispatch and before top-level tool bodies. The storage contract distinguishes an accepted append from its durability barrier. Nested programmatic calls rely on the recorded outer intent. These mechanisms help recover what was requested, but a crash between an external effect and its result commit still leaves an uncertain outcome. [D8]

The local sandbox expresses a file-effect policy. The inspected Linux profile mounts the host filesystem read-only and opens selected writable areas; its arguments do not create a network-isolated namespace. The macOS profile starts with broad allowance and restricts file writes. Its enforcement level must therefore be read relative to that filesystem policy. It does not establish universal read, network, credential, or trusted-plugin isolation. [D9]

Compaction similarly separates guarantees. DeepSeek can prune tool output, summarize a prefix, retain source references, and replace the active context projection while keeping audit history. Pairing and size reduction are mechanical properties; a fluent smaller summary is not proof that it preserves all decision-relevant evidence. [D10]

### 3.7 Scientific interpretation

DeepSeek is a useful study in component lifecycle, explicit effect boundaries, and reconstructable decision inputs. Its strongest contribution to the broader inquiry is showing that the agent loop can itself be a replaceable component in a larger computational system. The source does not establish that arbitrary plugin accumulation improves results or that the current minimal preset is specifically identical to the model's training harness.

A cross-project detail matters: its Pi adapter depends on @earendil-works/pi-ai. The inspected base mounts that adapter dormant until configured. DeepSeek and Pi therefore overlap at a reusable provider layer; they are not wholly independent technical stacks. [D11]

## 4. Pi: separate the controller from its representations

### 4.1 Current Pi includes two distinct runtime paths

The conventional coding-agent SDK constructs SessionManager, Agent, and AgentSession. Its ordinary path uses the core agent loop and JSONL session history. The current repository also includes Pi Durable, a separate reusable runtime for durable conversations, tasks, and application documents. It is not a drop-in persistence switch that silently strengthens every CLI session. [P1] [P8]

This distinction is essential when reading a monorepo. A package existing beside the CLI does not mean the CLI instantiates it. A feature being available does not mean it is enabled. The same caution applies to optional Codemode and external execution environments.

### 4.2 The small loop contains real scheduling decisions

The core loop prepares context, converts messages for the model, consumes a response, executes its tool batch, appends results, and evaluates continuation. It maintains separate steering and follow-up queues. Steering is considered before the next response, after the current tool batch finishes. Follow-up is admitted when the run would otherwise stop. [P2]

That makes steering a defined admission policy rather than a vague interrupt. Current source also polls after expensive preparation to catch newly arriving steering without accidentally violating one-at-a-time queue semantics. These details determine whether a correction takes effect at the right boundary.

The current default tool strategy is parallel. If any called tool requests sequential execution, the entire batch is serialized. In a parallel batch, completion events arrive as work finishes, while final transcript results retain source order. This does not infer dependencies between arbitrary calls. A producer-consumer dependency still has to be encoded explicitly. [P2]

A particularly instructive guard rejects every tool call from a length-truncated response. Salvaged JSON might be valid but incomplete. Pi uses the response termination reason as evidence that executing the proposal could be wrong. This illustrates why schema validity and completed intent are separate properties.

### 4.3 Provider normalization is a compiler-like boundary

Pi's model layer transforms a shared conversational representation into provider-compatible messages. It normalizes tool-call identifiers, repairs unresolved call/result bookkeeping, handles unsupported images, and removes incompatible reasoning blocks. In the inspected implementation, thinking from another model is dropped rather than treated as an ordinary visible answer. [P3]

Models can consequently share explicit work products, user goals, tool outputs, and saved notes, but a common message API is not a mechanism for transferring internal computation. Switching providers can change information content and behavior even when both accept the request. Compatibility, capability, calibrated confidence, and efficiency are four separate questions.

The compiler analogy is useful but limited: the adapter maps representations and protocols; it does not prove semantic equivalence across models. Protocol normalization itself needs tests. Repaired arguments also need provenance, because the arguments eventually executed may differ from what the model originally emitted.

### 4.4 Conversation history is a tree with derived views

SessionManager stores entries with IDs and one parent pointer. Selecting a leaf selects a conversation branch. This is a tree, or collection of rooted trees, rather than an arbitrary multi-parent knowledge graph. The current branch is then projected through compaction and omission/replacement edits to create model input. [P4]

Three states must remain distinct: the complete recorded history, the selected branch, and the current model-visible projection. A fact being recorded on disk does not mean it is in the current prompt. A failed attempt omitted from the prompt can remain useful for audit and cost accounting.

Branching the conversation does not rewind the working directory. If a branch assumes an older file version, the agent must inspect the current files or use an explicitly corresponding worktree/snapshot. This is an example of why conversational continuity and environmental continuity cannot be conflated.

Compaction introduces another bottleneck before summarization: the inspected serialization path truncates each tool result to 2,000 characters. A summarizer cannot preserve evidence it never receives. Repeatedly summarizing earlier summaries can compound omissions. The relevant metric is whether correct future decisions survive, not merely the reduction in tokens. [P5]

### 4.5 Extensions are trusted code

Pi explicitly places default filesystem, process, network, and credential authority at the launching process's user boundary. Project trust controls resource loading; it is not an operating-system sandbox. Extensions run inside the process and can alter tools, inputs, context, and provider payloads. [P6]

A narrow hook can block an individual tool, but trusted extension code can use host APIs outside that tool interface. Protecting only model-dispatched operations therefore cannot confine arbitrary plugin code. This is an architectural trust choice, not evidence of an accidental bypass.

Built-in edit/write operations coordinate through a process-local queue keyed by resolved file path. That protects a useful class of same-process mutation races; it does not coordinate separate processes, human editors, or shell commands that write directly. Cancellation after a completed write can also produce an aborted outcome while the file has already changed. [P7]

### 4.6 Codemode separates computation from model traffic

Pi's optional coding-agent Codemode runs JavaScript in QuickJS, with host effects exposed through selected tools instead of direct Node filesystem or networking APIs. Scripts can retrieve data, run independent operations concurrently, filter or join results, and return selected observations. [P9]

This can use the model for constructing a compact program and ordinary computation for executing it. However, a sandboxed interpreter invoking a powerful host tool still causes powerful effects. A failed script does not undo effects already completed. The small branch-aware store has different commit semantics from external tool execution; treating both as one transaction would be wrong.

### 4.7 Pi Durable makes recovery obligations explicit

Durable represents a tool as a task with a recorded execution checkpoint. The code resolves the tool, validates arguments, runs hooks, validates again, commits the actual arguments and replay policy, then executes. On recovery, it reruns only if both the stored policy and currently installed tool policy declare replay safe. Otherwise it explicitly records that the tool may have partially run. [P8]

This is a stronger formulation of the uncertain-outcome problem. A replay-safe label is still a contract with the tool implementation and target system; it cannot make a non-idempotent remote operation idempotent. The replay environment also matters: recorded arguments do not automatically freeze the working directory, implementation, credentials, or external state.

Durable Codemode records runtime identity, deterministic inputs, and a journal of delivered results. Recovery reexecutes control flow against recorded results and checks for divergence. That can resume internal computation without repeating every completed nested call. It still cannot eliminate a crash window between an external effect and its committed result. [P10]

Storage is conditional: the documented SQLite mode uses WAL with synchronous NORMAL; JSONL supports optional fsync; memory storage has no persistence. The runtime's ownership model is one process per storage, not an automatically distributed multi-writer society. [P11]

### 4.8 Scientific interpretation

Pi is especially useful for learning where representation ends and execution semantics begin. Its conventional agent path makes the controller understandable; Durable shows what additional machinery is needed when interrupted work must be recovered. The key lesson is to keep proposed, admitted, started, observed, recorded, and reconciled operations distinct. A larger monorepo does not erase these boundaries.

## 5. Codex: coherence across a continuing execution

### 5.1 The public source now has a distributed internal structure

The current core is Rust, with the main turn logic in core/src/session/turn.rs and separate modules for context, tool execution, providers, thread storage, and agent control. Public app-server and SDK interfaces let applications use that runtime without reproducing its user interface. Model access and managed services remain separate from the open harness. [C1] [C10]

Rust is relevant to local implementation correctness and resource ownership. It does not explain a model's reasoning quality or prove faster end-to-end task completion. For a model-driven task, network latency, generated tokens, tool runtimes, repeated mistakes, and verification can dominate local dispatch costs.

### 5.2 Each request captures a coherent view

The turn loop admits pending input, records it, captures a StepContext, constructs the next model input, performs sampling and tool execution, and decides whether tools, new input, or stop hooks require continuation. StepContext binds one immutable settings version to the advertised tools, model information, environment snapshot, and MCP connections for that request. [C1] [C2]

The subtlety is that tool callbacks retain the step that advertised them, including callbacks from a yielded code-mode execution. They should not silently switch to a newly configured tool with a different meaning. At the same time, live permission grants remain associated with the originating turn and current execution path. A frozen tool catalog must not become perpetual authority.

This resembles snapshot consistency in a database: readers operate against a coherent internal view. It does not snapshot every file or external service. If another worker edits a file during inference, the model's observation can still be stale. External preconditions need their own checks.

### 5.3 Execution separates dispatch from authority

ToolOrchestrator coordinates approval requirements, sandbox selection, execution, and retries after sandbox denial. The inspected implementation distinguishes the authority of the first attempt from an escalated retry. An approval for a constrained attempt cannot simply be reused to justify a more powerful execution. Some policy modes prohibit the retry. [C3]

This is more consequential than asking the model to remember a safety rule. The runtime can prevent an operation independently of whether the generator would comply with a prompt. Yet an approval decision, especially one involving another model, remains fallible; it is not semantic proof that an action is safe or useful.

The platform-specific confinement mechanisms and configured profiles also matter. The Linux paths include bubblewrap and supported legacy Landlock behavior; macOS uses Seatbelt; Windows has separate implementations and supported policy subsets. A custom or remote tool has its own enforcement boundary. It would be inaccurate to attribute one uniform security theorem to every possible Codex tool and deployment. [C4]

### 5.4 Parallelism preserves both lifecycle and observation

The tool runtime uses a shared read/write lock as an admission gate. Tools declared parallel-capable can hold shared access; exclusive tools hold exclusive access. The sampling path gathers in-flight results in order. A cancellation path coordinates terminal outcomes and avoids reporting an ordinary result twice. [C5]

This provides structured execution rather than arbitrary fire-and-forget concurrency. It still relies on correct declarations and effect semantics. A lock inside one runtime does not serialize all actors that can touch the workspace. Killing a future cannot undo an API mutation that already happened.

Code mode adds a broker between executable cells and ordinary tool dispatch. The originating step is retained, nested calls receive tracing and policy treatment, and execution can yield and later resume through the public lifecycle. This is a first-class computation interface around tools rather than a source of free correctness. [C6]

### 5.5 History, metadata, and compaction have separate jobs

The ThreadStore boundary distinguishes canonical history appends from explicit metadata updates. Its local implementation uses JSONL rollout history and SQLite metadata when available. Active sessions use LiveThread to apply persistence policy without depending on a particular backing store. [C7]

The current source also supports speculative background compaction under specific feature and provider conditions. It captures the history version, model identity, compaction identity, and authentication generation. Prepared results must match the relevant history generation, and prefix installation validates the candidate before replacing live history. Stale work can be discarded while still consuming resources. [C8]

This is a useful engineering response to expensive asynchronous summarization. It improves consistency of adoption; it does not prove the summary's semantic adequacy. Lower foreground latency can trade against wasted speculative work. Both costs belong in an evaluation.

Transcript normalization can insert synthetic aborted outputs for missing call results. This repairs the model protocol, but an aborted record is not proof that the external side effect never happened. Recovery still needs fresh observation when the effect state is uncertain. [C9]

### 5.6 Multi-agent support is resource management

Current agent-control code separates execution capacity, resident child runtimes, mailboxes, spawn/fork behavior, permissions, and shared budget accounting. The V2 path can unload idle child runtimes while preserving state and pending mail. Its guarantees depend on that configured backend and lifecycle; they should not be generalized to every historical multi-agent mode. [C11]

The conceptual contribution is ownership. A child consumes resources, has an identity and context boundary, can receive messages, and must eventually settle or be cancelled. Spawned reasoning is therefore a scheduling and recovery problem as well as an intelligence problem. This is closer to managing processes and jobs than to assigning biological names to agent roles.

### 5.7 Provider abstraction has a boundary

The inspected provider wire enum accepts Responses, and explicitly rejects the removed chat-completions wire option. Custom provider integration therefore depends on compatible protocol and capability support. This differs from assuming that changing an endpoint makes every model interchangeable. Native configuration comparisons and controlled same-model experiments must record these asymmetries. [C12]

### 5.8 Scientific interpretation

Codex is a valuable reference for the engineering that accumulates when an agent must remain coherent across user steering, asynchronous execution, changing policy, multiple interfaces, and long histories. The quantity of such machinery is not itself evidence of superior task accuracy. Its value must be assessed through the failures it prevents and the overhead it introduces.

## 6. The common ideas revealed by all three

### 6.1 Tools are an action language

A tool catalog behaves like an instruction set. Schemas constrain representation. A dispatch system gives those instructions operational meaning. Code mode composes them into larger programs. The model's effective problem changes when that language changes: ten separate model-mediated decisions can become one synthesized program orchestrating ten operations. Its control flow is explicit, while the tools retain their own failure and nondeterminism.

This is the connection to CodeAct: action representation and training for that representation are separate interventions. A model trained to use one tool language may perform differently when a harness changes that language. Expressiveness alone does not establish a better interface. [R3]

The correct objective is useful work per decision and per resource budget, while preserving evidence and controllable effects. Reducing tool count or prompt size in isolation can destroy observability or force more mistakes.

### 6.2 A summary is a derived view of evidence

Compression is useful only relative to future decisions. Consider two histories: in one, a deployment definitely failed before execution; in the other, it may have succeeded but its acknowledgement was lost. If both become the summary 'deployment failed', the system has erased the distinction needed for safe retry.

A good working representation preserves goals, constraints, current observations, evidence identities, unresolved hypotheses, pending effects, and known unknowns. Retrieval can recover omitted detail if the source remains accessible. A summary that has lost both the evidence and its locator is harder to repair.

This is a task-conditioned information problem. A shorter summary is not necessarily a better summary. A longer context is not necessarily a better decision state. Evaluate whether correct actions remain distinguishable after transformation.

### 6.3 Persistence is not an external transaction

There are at least four distinct operations: append an event, commit it durably, cause an external effect, and confirm the intended postcondition. They may occur at different times and under different failure models.

For arbitrary remote mutations, one useful recovery model distinguishes requested, admitted, started, observed-success, observed-failure, and outcome-unknown states. Exactly-once effect claims require a defined boundary and supporting protocol, such as target-side deduplication or atomic coupling of a mutation and its operation record. Reconciliation can resolve uncertain outcomes or restore desired state; by itself, it does not guarantee that no duplicate effect occurred. A local journal cannot infer an unobserved external outcome.

Desired-state reconciliation illustrates this distinction. Success is established by observed convergence and preserved recovery paths. A successful function return is one observation, with a scope and an error model, rather than universal evidence that the goal has been achieved.

### 6.4 A hybrid system is not automatically strong symbolic reasoning

All three combine a learned proposal mechanism with explicit software control. In that broad sense, they are hybrid systems. Calling them neurosymbolic is only useful if the intended meaning is made explicit. Schemas, state machines, and interpreters do not automatically provide grounded symbolic concepts, sound deduction, or a calibrated model of the world.

A stronger engineering claim is testable: the runtime can preserve specified invariants even when the generator proposes something invalid. Replace the model with a deliberately bad proposer. Whatever still holds is evidence of an enforced runtime property; whatever disappears was dependent on model behavior or instructions.

### 6.5 Memory and improvement must be distinguished carefully

| Change | What it can do | What would establish improvement |
| --- | --- | --- |
| Current context | Change the next action without changing weights | Better continuation decisions on controlled histories |
| Retained experience | Supply evidence or procedures to later tasks | Better held-out performance with memory than without |
| Reusable skill | Change an explicit procedure or tool-use strategy | Benefits across new tasks, with procedure version pinned |
| Harness implementation | Change scheduling, representations, or controls | Mechanism ablation plus regression and integration checks |
| Model parameters | Change the learned policy | Controlled evaluation of training and generalization |

Memory-based adaptation can legitimately be learning without parameter updates. Merely recording experience does not establish that the experience will be retrieved, interpreted correctly, or improve future performance. Self-modification similarly requires a promotion rule and independent evidence, not simply the ability to edit source.

### 6.6 More agents change the topology, not the laws of correctness

Parallel workers can search independent subproblems, generate alternative candidates, or check a result. These are different uses. A communicating team adds messages, stale views, integration work, and potential correlated mistakes. Independent candidate sampling is an important baseline because extra inference can otherwise be mistaken for an advantage from coordination.

The current revision of the scaling-agents study supports task-dependent coordination effects. Its experiments do not establish one universally optimal topology or a general threshold after which agents stop helping. [R4]

Agents responding to signals can use an event-driven design. It does not require a centralized semantic router. It still needs task ownership, arbitration, budget admission, stale-result rejection, and a rule for who can commit a mutation. A shared work board with claims or leases is one possible mechanism; beneficial self-organization is a hypothesis to test.

## 7. What the research establishes and what it leaves open

SWE-agent is direct evidence that an agent-computer interface matters. With GPT-4 Turbo fixed on its SWE-bench Lite evaluation, the complete interface resolved 18% versus 11% for the shell-only baseline with a demonstration. The relevant inference is that action and observation design can change outcomes; its historical settings are not permanent optima for current models. [R5]

CaMeL offers a concrete security direction: separate trusted planning from untrusted information handling and enforce value-flow policy in an interpreter. That is stronger than simply hoping two models will supervise one another. Its guarantees depend on the specified policies and threat model; the architecture also has utility and resource costs. [R6]

Anthropic's infrastructure experiment held the model, harness, and tasks constant while changing resource limits on Terminal-Bench 2.0. Strict versus uncapped resources differed by six percentage points. CPU/RAM allocation and timeout policy can therefore explain part of an apparent agent improvement. [R7]

An evaluator also needs evaluation. A recent research-agent reward-hacking study shows that plausible artifacts and reported scores can miss invalid methods under its tested conditions. That finding does not estimate misconduct in these three harnesses. It motivates keeping agent-produced evidence separate from independently reproduced acceptance results. [R8]

These studies support particular mechanisms and failure modes. They do not measure which of the three source snapshots reviewed here will best solve a particular Rust, Python, or infrastructure workload. There is also no source-level route to proving an LLM's internal reasoning from a transcript.

## 8. How to assemble the concept into an engineering program

### 8.1 Begin with contracts rather than a list of roles

For a small research substrate, I would define six boundaries: Task, Context, Proposal, Effect, Evidence, and Evaluation. Each can be implemented behind a narrow interface and instrumented without exposing its internals to callers.

Task carries the objective, constraints, acceptance conditions, and budget. Context selects evidence and memory while retaining provenance. Proposal is an untrusted candidate operation or answer. Effect admits and executes a scoped operation, recording its actual arguments and uncertain outcomes. Evidence names observations and their conditions. Evaluation decides whether the goal is sufficiently established for the task.

A useful action record could include an action ID, target identity, authority scope, preconditions, exact arguments, replay classification, and expected evidence. A result record should link to that action and preserve the difference between observed success, observed failure, and an unknown outcome. This is a proposed contract, not an API implemented identically by the reviewed systems.

### 8.2 Invariants to keep outside model persuasion

- A request's advertised operation identity stays tied to its execution; current authority is still checked.
- Every started child or tool has an owner, a settlement path, and defined cancellation behavior.
- A summary retains evidence identities; authoritative structured records preserve observation status independently of generated prose.
- A missing acknowledgement does not automatically authorize replay of a non-idempotent operation.
- The component proposing a result does not have sole authority to redefine acceptance or falsify its measurements.
- A saved procedure or runtime change is promoted only after a versioned, independent evaluation appropriate to its scope.

Summary transformations should also retain decision-relevant uncertainty. That semantic requirement needs evaluation against controlled histories; fluent text does not establish fidelity. These boundaries translate cleanly to a Rust implementation using enums for explicit states, traits for effect ports, owned tasks for concurrency, and an append-only evidence ledger or transactional store. Neither Rust nor hexagonal structure supplies the semantics automatically. The implementation and tests must establish the mechanical invariants, while semantic adequacy requires task-level evidence.

### 8.3 Add specialized representations for specific jobs

Embeddings can propose semantically related evidence. A reranker can improve ordering of candidates. A graph can represent dependencies and provenance. A symbolic engine can enforce a specified constraint or derive consequences under a formal model. An LLM can interpret ambiguous goals and propose plans. A code interpreter can execute loops and reductions. An external verifier can test a postcondition.

These are different computational roles, not substitutes on one intelligence scale. Their value depends on concrete failure signatures. A graph of unsupported claims remains unsupported. Semantic similarity does not establish truth. A formal solver is only as relevant as its formalization. Adding components before identifying the missing capability creates integration work without an established benefit.

### 8.4 Use two experiments instead of one confused comparison

First compare complete systems in their intended configurations. That answers which product is useful for the selected workload. Then run mechanism experiments with a common supported model, environment, tools, budget, and task distribution. That addresses why. Unsupported model/protocol combinations should remain unsupported cells rather than being silently emulated as equivalent.

Start with a diagnostic set spanning local bug repair, cross-module changes, long histories, interrupted tools, conflicting writes, and infrastructure reconciliation. A small pilot is for finding failure classes, not claiming a narrow leaderboard victory. Use repeated trials, pair comparisons by task, and keep fresh tasks held out for promotion decisions.

| Experiment | Intervention | Primary observations |
| --- | --- | --- |
| Action representation | Direct tools versus executable composition | Verified success, model turns, invalid calls, retained evidence |
| Context | Full history versus compaction versus evidence-linked summary | Constraint retention, false certainty, repeated failed work |
| Recovery | Crash before effect, after effect, and before result commit | Duplicate mutations, lost work, correctly preserved uncertainty |
| Concurrency | Ordered versus out-of-order completion and conflicting work | Actual postconditions, transcript consistency, latency |
| Verification | Model review, executable checks, independent checker | False acceptance and rejection on seeded defects |
| Coordination | One agent, independent candidates, communicating team | Selected-result success, integration cost, total resource use |
| Component change | Restart or replace a service during active work | Stale bindings, leaked resources, lost mail, recovery time |

Record model identity and settings, task/repository commit, harness commit, effective tool catalog, prompts, environment digest, CPU/RAM guarantees and ceilings, network policy, timeouts, cache conditions, all workers' usage, and evaluator revision. Equal tokens, equal dollars, and equal wall time answer different questions. Compare several budgets rather than treating one arbitrary point as universal.

Useful outcomes are verified success, cost per attempted task, cost per verified success, time to a verified result, intervention count, repair cycles, and failure class. Include speculative work, discarded samples, and failed calls in costs. If there are no verified successes, cost per success is undefined or unbounded, not zero.

The falsification rule is practical: retain a component when its benefit survives an appropriate simpler baseline and repays its information, latency, coordination, and maintenance costs on the intended task distribution. Some properties, such as a mandatory authority boundary, are hard constraints rather than metrics to trade away.

## 9. A source-reading route

Read Pi's core loop first to understand the irreducible control structure. Follow a message through transformation and session projection. Then read Pi Durable's tool task to see what a recoverable effect requires. Next read DeepSeek's Cordis lifecycle and request construction to understand replacement and reconstructability. Finish with Codex's StepContext, orchestrator, and compaction installation to study the consistency obligations that appear in a broad application runtime.

For each function, ask: what state does it own; what can run concurrently; what evidence enters the log; what has already happened when an error is returned; what is restored after a crash; and what property depends only on a prompt? These questions reveal more than reading the marketing feature list.

### Source references: DeepSeek

- **[D0]** Repository snapshot and release manifests: https://github.com/deepseek-ai/deepseek-harness/tree/687f282e8625c6b8d11ff58211a90524be2e4317

- **[D1]** Product composition: packages/bundle/base/cordis.patch.yml — [source 1](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/bundle/base/cordis.patch.yml)

- **[D2]** Component lifecycle and cleanup: vendor/cordis/src/fiber.ts; service registration: vendor/cordis/src/service.ts; vendoring qualifications: vendor/README.md — [source 1](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/vendor/cordis/src/fiber.ts); [source 2](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/vendor/cordis/src/service.ts); [source 3](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/vendor/README.md)

- **[D3]** Turn, step, and frozen request construction: packages/core/agent-loop/src/agent.ts, especially 615-703 — [source 1](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/agent.ts)

- **[D4]** Adapter registration and dispatch: packages/llm/llm/src/index.ts, especially 945-1013 — [source 1](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/llm/llm/src/index.ts)

- **[D5]** Parallel and exclusive tool scheduling: packages/core/agent-loop/src/tool-calls.ts — [source 1](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/tool-calls.ts)

- **[D6]** Nested programmatic tool dispatch: packages/core/tools/src/ptc.ts — [source 1](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/tools/src/ptc.ts)

- **[D7]** Node interpreter boundary: packages/ptc-runtime/ptc-runtime-node/src/index.ts; environment.ts; bootstrap.ts — [source 1](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/ptc-runtime/ptc-runtime-node/src/index.ts); [source 2](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/ptc-runtime/ptc-runtime-node/src/environment.ts); [source 3](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/ptc-runtime/ptc-runtime-node/src/bootstrap.ts)

- **[D8]** Durability checkpoints: packages/session/session-checkpoint-policy/src/index.ts; storage contract: packages/session/session-persistence/src/handle.ts — [source 1](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-checkpoint-policy/src/index.ts); [source 2](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-persistence/src/handle.ts)

- **[D9]** Filesystem confinement profiles: packages/sandbox/sandbox-local/src/profiles.ts — [source 1](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/sandbox/sandbox-local/src/profiles.ts)

- **[D10]** Compaction and source replacement: packages/compaction/compaction-basic/src/region.ts; packages/compaction/compaction-basic/src/index.ts; pruning: packages/compaction/compaction-tool-result-pruner/src/index.ts — [source 1](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/compaction/compaction-basic/src/region.ts); [source 2](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/compaction/compaction-basic/src/index.ts); [source 3](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/compaction/compaction-tool-result-pruner/src/index.ts)

- **[D11]** Pi provider dependency: packages/llm/llm-pi-ai/package.json; dormant configuration: packages/bundle/base/cordis.patch.yml — [source 1](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/llm/llm-pi-ai/package.json); [source 2](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/bundle/base/cordis.patch.yml)

### Source references: Pi

- **[P0]** Repository snapshot and identity: https://github.com/earendil-works/pi/tree/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03

- **[P1]** Coding-agent runtime construction: packages/coding-agent/src/core/sdk.ts — [source 1](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/coding-agent/src/core/sdk.ts)

- **[P2]** Core loop and scheduling: packages/agent/src/agent-loop.ts; default strategy and queues: packages/agent/src/agent.ts — [source 1](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/agent/src/agent-loop.ts); [source 2](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/agent/src/agent.ts)

- **[P3]** Cross-provider message transformation: packages/ai/src/api/transform-messages.ts — [source 1](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/ai/src/api/transform-messages.ts)

- **[P4]** Session tree and model projection: packages/coding-agent/src/core/session-manager.ts — [source 1](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/coding-agent/src/core/session-manager.ts)

- **[P5]** Compaction input serialization: packages/coding-agent/src/core/compaction/utils.ts — [source 1](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/coding-agent/src/core/compaction/utils.ts)

- **[P6]** Default trust boundary: SECURITY.md; README.md — [source 1](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/SECURITY.md); [source 2](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/README.md)

- **[P7]** Mutation queue: packages/coding-agent/src/core/tools/file-mutation-queue.ts — [source 1](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/coding-agent/src/core/tools/file-mutation-queue.ts)

- **[P8]** Durable tool intent and replay: packages/durable/src/harness/tool.ts — [source 1](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/durable/src/harness/tool.ts)

- **[P9]** Coding-agent Codemode: packages/coding-agent/docs/codemode.md — [source 1](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/coding-agent/docs/codemode.md)

- **[P10]** Durable Codemode journal: packages/durable/src/codemode/codemode.ts — [source 1](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/durable/src/codemode/codemode.ts)

- **[P11]** Durable storage and ownership: packages/durable/README.md — [source 1](https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/durable/README.md)

### Source references: Codex

- **[C0]** Repository snapshot: https://github.com/openai/codex/tree/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857

- **[C1]** Turn admission, sampling, and continuation: codex-rs/core/src/session/turn.rs — [source 1](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/session/turn.rs)

- **[C2]** Request-scoped settings and tools: codex-rs/core/src/session/step_context.rs — [source 1](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/session/step_context.rs)

- **[C3]** Approval, sandboxing, and retry: codex-rs/core/src/tools/orchestrator.rs — [source 1](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/tools/orchestrator.rs)

- **[C4]** Platform enforcement contract: codex-rs/core/README.md; implementations: codex-rs/sandboxing — [source 1](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/README.md); [source 2](https://github.com/openai/codex/tree/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/sandboxing)

- **[C5]** Tool concurrency and cancellation: codex-rs/core/src/tools/parallel.rs — [source 1](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/tools/parallel.rs)

- **[C6]** Code-mode dispatch broker: codex-rs/core/src/tools/code_mode/delegate.rs — [source 1](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/tools/code_mode/delegate.rs)

- **[C7]** Thread storage boundary: codex-rs/thread-store/README.md — [source 1](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/thread-store/README.md)

- **[C8]** Background compaction and installation: codex-rs/core/src/session/async_compaction.rs; codex-rs/core/src/compact_remote_v2_installation.rs — [source 1](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/session/async_compaction.rs); [source 2](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/compact_remote_v2_installation.rs)

- **[C9]** Transcript normalization: codex-rs/core/src/context_manager/normalize.rs — [source 1](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/context_manager/normalize.rs)

- **[C10]** Official integration overview: https://developers.openai.com/blog/codex-as-a-platform

- **[C11]** Agent lifecycle: codex-rs/core/src/agent/control/execution.rs; residency.rs; mailbox.rs; budget.rs — [source 1](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/agent/control/execution.rs); [source 2](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/agent/control/residency.rs); [source 3](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/agent/control/mailbox.rs); [source 4](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/agent/control/budget.rs)

- **[C12]** Provider protocol: codex-rs/model-provider-info/src/lib.rs — [source 1](https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/model-provider-info/src/lib.rs)

### Scientific and experimental references

- **[R1]** Yao et al., ReAct: Synergizing Reasoning and Acting in Language Models, ICLR 2023: https://arxiv.org/abs/2210.03629

- **[R2]** Shi et al., A Programming Paradigm for Spatiotemporal Composability, August 2026: https://arxiv.org/abs/2608.25512. Reversibility and mediation limits: sections 4.3.2 and 6.1-6.3.

- **[R3]** Wang et al., Executable Code Actions Elicit Better LLM Agents, ICML 2024: https://proceedings.mlr.press/v235/wang24h.html

- **[R4]** Towards a Science of Scaling Agent Systems, revised April 2026, version 3: https://arxiv.org/html/2512.08296v3

- **[R5]** Yang et al., SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering, NeurIPS 2024: https://arxiv.org/html/2405.15793v3

- **[R6]** Debenedetti et al., Defeating Prompt Injections by Design, 2025: https://arxiv.org/html/2503.18813v2

- **[R7]** Anthropic, Quantifying infrastructure noise in agentic coding evals, February 2026: https://www.anthropic.com/engineering/infrastructure-noise

- **[R8]** Huang et al., Reward Hacking Challenges Oversight of Autonomous Research Agents, September 2026 preprint: https://arxiv.org/html/2609.28614v1

### Representative tests inspected

DeepSeek: packages/core/agent-loop/tests/properties.spec.ts (generated short input sequences and FIFO behavior); request-reconstruction.spec.ts (reconstructed mocked requests); tool-calls.spec.ts (out-of-order completion, ordered observations, bounded concurrency).

Pi: packages/agent/test/agent-loop.test.ts (truncated proposals, trusted hook mutation, batch order and steering); packages/ai/test/transform-messages-cross-model-thinking.test.ts; packages/durable/test/harness-tools-recovery.test.ts (safe/unsafe replay and interruption).

Codex: codex-rs/core/tests/suite/pending_input_persistence.rs (persistence checkpoints before subsequent requests); codex-rs/core/src/compact_remote_v2_installation_tests.rs (stale prepared compaction); codex-rs/core/tests/suite/guardian_retry.rs (approval and stale authority).

These test bodies were inspected but not run. They provide executable specifications of intended boundary behavior; they are not newly observed passing results, universal proofs, or comparative task-quality measurements.

## 10. Final judgment

The most productive synthesis is learned proposal with explicit software control, evidence-preserving state, and bounded effects. DeepSeek is a strong source for thinking about runtime composition. Pi is a strong source for understanding separation of representations and for contrasting a conversational controller with durable task execution. Codex is a strong source for studying coherence across a continuing, policy-governed application runtime. Those judgments concern the usefulness of the code as architectural evidence, not a measured winner.

For compositional-intelligence, the next valuable step would be a small instrumented test environment that isolates one boundary at a time. Start with a task that has an unambiguous external postcondition and an injected interruption. Then compare how each system preserves the goal, records what happened, represents uncertainty, resumes, and proves completion. That experiment connects the broad concept to observable machinery and gives later additions a reason to exist.

[C10]: https://developers.openai.com/blog/codex-as-a-platform
[R1]: https://arxiv.org/abs/2210.03629
[R2]: https://arxiv.org/abs/2608.25512
[R3]: https://proceedings.mlr.press/v235/wang24h.html
[R4]: https://arxiv.org/html/2512.08296v3
[R5]: https://arxiv.org/html/2405.15793v3
[R6]: https://arxiv.org/html/2503.18813v2
[R7]: https://www.anthropic.com/engineering/infrastructure-noise
[R8]: https://arxiv.org/html/2609.28614v1
[D1]: https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/bundle/base/cordis.patch.yml
[D2]: https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/vendor/cordis/src/fiber.ts
[D3]: https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/agent.ts
[D4]: https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/llm/llm/src/index.ts
[D5]: https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/tool-calls.ts
[D6]: https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/tools/src/ptc.ts
[D7]: https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/ptc-runtime/ptc-runtime-node/src/index.ts
[D8]: https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-checkpoint-policy/src/index.ts
[D9]: https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/sandbox/sandbox-local/src/profiles.ts
[D10]: https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/compaction/compaction-basic/src/region.ts
[D11]: https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/llm/llm-pi-ai/package.json
[P1]: https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/coding-agent/src/core/sdk.ts
[P2]: https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/agent/src/agent-loop.ts
[P3]: https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/ai/src/api/transform-messages.ts
[P4]: https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/coding-agent/src/core/session-manager.ts
[P5]: https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/coding-agent/src/core/compaction/utils.ts
[P6]: https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/SECURITY.md
[P7]: https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/coding-agent/src/core/tools/file-mutation-queue.ts
[P8]: https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/durable/src/harness/tool.ts
[P9]: https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/coding-agent/docs/codemode.md
[P10]: https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/durable/src/codemode/codemode.ts
[P11]: https://github.com/earendil-works/pi/blob/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03/packages/durable/README.md
[C1]: https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/session/turn.rs
[C2]: https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/session/step_context.rs
[C3]: https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/tools/orchestrator.rs
[C4]: https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/README.md
[C5]: https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/tools/parallel.rs
[C6]: https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/tools/code_mode/delegate.rs
[C7]: https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/thread-store/README.md
[C8]: https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/session/async_compaction.rs
[C9]: https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/context_manager/normalize.rs
[C11]: https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/core/src/agent/control/execution.rs
[C12]: https://github.com/openai/codex/blob/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857/codex-rs/model-provider-info/src/lib.rs
[D0]: https://github.com/deepseek-ai/deepseek-harness/tree/687f282e8625c6b8d11ff58211a90524be2e4317
[P0]: https://github.com/earendil-works/pi/tree/d2e7d8b7c1d31d3661f769d5caef7ba8d50c3e03
[C0]: https://github.com/openai/codex/tree/4e7b9e285ba4ac6ce18ca452cf9e88d3d75ec857
