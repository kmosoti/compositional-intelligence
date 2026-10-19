# Operational coordination records

This directory is initially empty of operational JSON. No live task, admission, review, resource reservation, or scientific result is asserted by the synthetic files in [examples/](../examples/README.md).

When a real bounded task is ready to use the manual record format, preserve its reviewed records here with `schema_version: 1` and `demonstration: false`. Follow the [format](../examples/README.md) and [coordination contract](../../../docs/coordination.md). Preserve the admitted specification, exact subject identities, and review provenance in appropriate versioned artifacts. Do not copy fixture digests or invent authorization/acceptance to populate a board.

The default `python3 -B scripts/check_coordination.py` recursively reads all JSON under this directory as one collection. Include full task histories and pinned prerequisite records; the checker currently has no compacted-checkpoint format. Keep conceptual research links separate from execution prerequisites. A recorded author, timestamp, or receipt is a claim requiring real provenance, not an authentication mechanism.

Accepted revisions are preserved, with successors linked by the canonical predecessor digest. Integrate through the named integrator and reviewed Git history; do not edit an old accepted record silently. Retain referenced commits and evidence, including failed attempts. A schema change requires an explicit compatibility/migration decision and corresponding validation.

The first operational exercise should measure whether this record cost improves coordination. The directory's existence and an empty successful discovery are not evidence that the protocol has been exercised in practice.
