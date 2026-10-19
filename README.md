# Compositional Intelligence

**Finite means. Novel compositions. Measured intelligence per unit of computation.**

A research and experimentation project combining the science of intelligence with the engineering of systems that learn, represent, reason, and act. It investigates whether combinations of neural models, retrieval, symbolic computation, probabilistic inference, graphs, memory, and other mechanisms produce transferable competence and useful capability under bounded resources. Rust and consumer hardware are the current implementation starting points.

**Status: inception / research infrastructure.** No cognitive system has been demonstrated, benchmarked, trained, or released here. All proposed mechanisms remain hypotheses. There are **no release milestones or alpha versions**.

## Research question

What is the smallest set of complementary computational mechanisms that can acquire and preserve useful evidence, compose unfamiliar solutions, test consequences, select actions and adapt to experience while minimizing expensive autoregressive generation?

The linguistic idea of making unbounded use of finite means motivates tests of **compositional generalization**, not an assumption of intelligence.

## What governs the project

**Research → experiments → analysis → revised research governs the technical direction. The code is not an oracle.** The current architecture can change rapidly, including substantial replacement, when evidence or a better experiment justifies it. Existing code describes a present instrument; it does not determine what the science must conclude.

Freeze the protocol and relevant versions for a particular comparison, preserve its evidence, and revise the next experiment openly. A green test establishes only the behavior it exercises. It cannot make a cognitive theory true. See the [research program](docs/research-program.md) and [governance decision](docs/adr/0002-research-governs-implementation.md).

## Research principles

1. Measure against simple, competitive baselines appropriate to the question; a quantized SLM with retrieval and deterministic tools is the current starting comparator.
2. Treat neural, neuro-symbolic, hyperdimensional, graph and probabilistic mechanisms as competing *candidates*, not compulsory modules.
3. Separate facts, inference, hypotheses, predictions and unknowns. Keep source/provenance references.
4. Compare end-to-end correctness, held-out generalization, latency, memory, energy and total cost, not attractive architectural diagrams.
5. Admit negative results and reject mechanisms that fail controlled comparison.
6. Separate agent-produced patches from independent acceptance and scientific interpretation.
7. Record the starting machine: RTX 3060 Laptop GPU (6 GB), 32 GB RAM, Intel i7-10750H. Verify actual limits and report which conclusions depend on this resource envelope.
8. Separate task capability, transfer, learning, metacognition, conscious access, and subjective experience. No architecture label or benchmark score settles all of them.

## Start here

- [Research charter](docs/research-charter.md)
- [Integrated research program](docs/research-program.md)
- [David Krakauer: intelligence, understanding, and cognitive tools](docs/research/krakauer-intelligence.md)
- [DeepSeek Harness, Pi, and Codex: source review](docs/research/agent-harness-review.md)
- [Scientific method and experiments](docs/methodology.md)
- [Candidate architecture](docs/architecture.md)
- [Agent harness protocol](docs/agent-harness.md)
- [Research coordination contract](docs/coordination.md)
- [GitHub coordination: research and failure analysis](docs/research/github-coordination-review.md)
- [Agent instructions](AGENTS.md)
- [Research hypotheses](research/README.md)
- [Experiments](experiments/README.md)
- [Wiki source pages](wiki/Home.md)

## Repository organization

| Path | Role |
|---|---|
| `AGENTS.md` | Authoritative vendor-neutral instructions |
| `.agents/skills/` | Reusable Agent Skills, one focused `SKILL.md` each |
| `.agents/roles/` | Task profiles, not permanent agent hierarchy |
| `docs/` | Research program, literature and source reviews, methodology, architecture alternatives and engineering records |
| `research/` | Registered hypotheses and counterexamples |
| `experiments/` | Protocols, manifests, results and negative findings |
| `crates/` | Minimal Rust types only, not a validated cognition system |
| `harness/` | Process contracts and future controller interfaces |
| `wiki/` | Version-controlled GitHub Wiki source |
| `.github/` | Issue/PR templates and foundational CI |

## Development

Install Rust stable via rustup. The Cargo crates use edition 2024 and the unpublished placeholder package version `0.0.0`, which is *not* a product release.

```bash
cargo fmt --all --check
cargo test --workspace
cargo clippy --workspace --all-targets -- -D warnings
```

The [coordination and record guide](harness/coordination/README.md) documents the offline Python checks, experiment lifecycle, and clearly labeled synthetic examples. These checks exercise record consistency; no operational coordination records or experiment results are supplied by the examples.

This repo does not yet implement an autonomous agent controller, independent sandbox evaluator, deployed GitHub Project writer, model inference pipeline, benchmarking harness, or research result. Their contracts and experiments can be developed incrementally.

## Wiki

The GitHub Wiki is a separate Git repository. Pages live under `wiki/` and can be published using `bash scripts/publish_wiki.sh` from an authenticated workstation. This main-branch commit does not itself update the live Wiki.

## Contribution rules

Read [AGENTS.md](AGENTS.md). Open hypotheses and experiments before adopting an architecture. Report uncertainty, conflicting evidence and validation limits. No agent may self-certify results.

Licensed under the repository's existing MIT LICENSE.
