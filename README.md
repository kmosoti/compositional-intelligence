# Compositional Intelligence

**Finite means. Novel compositions. Measured intelligence per unit of computation.**

A Rust-first research project investigating whether heterogeneous combinations of compact neural models, retrieval, symbolic computation, probabilistic inference, graphs and associative representations can outperform a small language-model agent on consumer hardware.

**Status: inception / research infrastructure.** No cognitive system has been demonstrated, benchmarked, trained, or released here. All proposed mechanisms remain hypotheses. There are **no release milestones or alpha versions**.

## Research question

What is the smallest set of complementary computational mechanisms that can acquire and preserve useful evidence, compose unfamiliar solutions, test consequences, select actions and adapt to experience while minimizing expensive autoregressive generation?

The linguistic idea of making unbounded use of finite means motivates tests of **compositional generalization**, not an assumption of intelligence.

## Research principles

1. Measure against a simple, competitive baseline: a quantized SLM with retrieval and deterministic tools.
2. Treat neural, neuro-symbolic, hyperdimensional, graph and probabilistic mechanisms as competing *candidates*, not compulsory modules.
3. Separate facts, inference, hypotheses, predictions and unknowns. Keep source/provenance references.
4. Compare end-to-end correctness, held-out generalization, latency, memory, energy and total cost, not attractive architectural diagrams.
5. Admit negative results and reject mechanisms that fail controlled comparison.
6. Separate agent-produced patches from independent acceptance and scientific interpretation.
7. Optimize for the starting machine: RTX 3060 Laptop GPU (6 GB), 32 GB RAM, Intel i7-10750H. Verify actual device limits.

## Start here

- [Research charter](docs/research-charter.md)
- [Scientific method and experiments](docs/methodology.md)
- [Candidate architecture](docs/architecture.md)
- [Agent harness protocol](docs/agent-harness.md)
- [Agent instructions](AGENTS.md)
- [Research hypotheses](research/HYP-0001.md)
- [Experiments](experiments/README.md)
- [Wiki source pages](wiki/Home.md)

## Repository organization

| Path | Role |
|---|---|
| `AGENTS.md` | Authoritative vendor-neutral instructions |
| `.agents/skills/` | Reusable Agent Skills, one focused `SKILL.md` each |
| `.agents/roles/` | Task profiles, not permanent agent hierarchy |
| `docs/` | Methodology, architecture alternatives and engineering records |
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

This repo does not yet implement an autonomous agent controller, independent sandbox evaluator, model inference pipeline, benchmarking harness, or research result. Their contracts and experiments can be developed incrementally.

## Wiki

The GitHub Wiki is a separate Git repository. Pages live under `wiki/` and can be published using `bash scripts/publish_wiki.sh` from an authenticated workstation. This main-branch commit does not itself update the live Wiki.

## Contribution rules

Read [AGENTS.md](AGENTS.md). Open hypotheses and experiments before adopting an architecture. Report uncertainty, conflicting evidence and validation limits. No agent may self-certify results.

Licensed under the repository's existing MIT LICENSE.
