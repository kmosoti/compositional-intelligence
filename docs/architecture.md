# Candidate cognitive architecture (not adopted)

## Functional roles, not literal brain replicas
Perception/encoding, associative memory, relational knowledge, hypothesis generation, candidate evaluation, prediction, conflict detection and action execution are useful *problem decompositions*. They need not be separate neural models or crates.

## Mechanism candidates
- Sparse + dense search for retrieval. Embedding similarity does not establish truth.
- Cross-encoder reranking for precision; test its marginal gain and CPU cost.
- Graph + temporal/provenance edges for entities and relations. Separate asserted, derived and hypothesized edges.
- Symbolic solvers and Datalog for applicable exact constraints.
- Classical ML or small contrastive encoders for rapid familiar decisions; Laya/CLM are candidate comparisons, not mandates.
- Binary hyperdimensional vectors for compositional association; compare with feature hashing and embeddings.
- Compact predictive dynamics where sequential transition data exists.
- Quantized SLM for unfamiliar composition, interpretation and language expression.

## Representation boundary
Do not assume heterogeneous embeddings, HDC signatures and latent neural states are interchangeable. Keep immutable evidence IDs and typed representation identity/metric/normalization in adapters.

## Control plane
Signal-driven candidate generation and evaluation, with deterministic permissions and resource arbitration. This is not a magical absence of coordination. Agent/tool calls must be authorized; unknown or risky actions cannot bypass policy.

## Dependency architecture
Use hexagonal separation where it creates independently testable behavior or replaceable backend dependencies. Static specialization and zero allocation belong only in *measured* hotspots. Do not require every composite to own neither state nor algorithms.

## Falsifier
If a competitive SLM + retrieval + tools baseline exceeds composite quality/cost under equal conditions, reject unnecessary regions and revise the decomposition.
