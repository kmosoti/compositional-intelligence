# Coordination adoption: scope, observations, and cutover conditions

**Date:** 2026-10-19. **Repository baseline:** `92a73ad56f9f169c956ea202455d3a627238e53d`.

This record bounds the owner's request to research and mature the supplied GitHub coordination setup for this project. It is not a claim that a live Project, scheduler, or remote controller has been configured.

## Observed landscape

| Classification | Observation |
| --- | --- |
| Observed source | Existing worker/evaluator/controller contract, eight named task phases plus Blocked, research-driven architectural governance, four planned experiments, no autonomous executor/controller implementation |
| Observed API | Repository `kmosoti/compositional-intelligence`, default branch `main`, head matching the baseline above; connection reports repository push/admin permission |
| Observed API | All-state repository issue and PR collections returned zero items during this inventory; this does not establish absence of an account Project or draft Project items |
| Observed capability | This session's connector exposed repository read/write operations and no callable Project operation; repository `has_projects` is true |
| Documented | Current GitHub Projects REST/GraphQL and delivery/concurrency semantics in the [primary-source review](research/github-coordination-review.md) |
| Unknown | Live Project URL, owner type/number, fields/options, views, workflows, Project permissions, browser/native-app layout, deployed worker identities and shared-resource topology |
| Decision | Manual coordination plus versioned records and offline checks is the bounded baseline; no live Project binding is inferred |

## Bounded repository change plan

| Target | Preimage | Intended postimage | Recovery |
| --- | --- | --- | --- |
| Coordination contract, ADR, source review, adoption record | Absent | Versioned project-specific rules with evidence and capability limits | Reviewed successor/revert; retain rationale and evidence |
| `scripts/check_research.py` | Hard-coded inception assertion for EXP-0001 and a Rust crate | Discovery-based structural validation of evolving experiments | Compare against baseline and preserve any later records before rollback |
| Offline coordination checker, synthetic examples, focused tests | Absent | Read-only consistency checks; clearly labeled demonstrations | Remove/supersede by reviewed change; no production effects to undo |
| Agent instructions, harness guide, task/submission/failure templates, issue/PR templates | Existing instructions and templates | Links and fields for scope, evidence identity, negative outcomes, control uncertainty | Normal reviewed textual revision |
| CI research job | Structural check only | Existing structural check plus offline coordination and regression checks | Revert only the added steps if defective; do not weaken acceptance to make a candidate pass |
| `.gitignore` | Rust-oriented generated-file exclusions | Exclude local Python bytecode caches from these checks | Normal reviewed textual revision |
| Experiment manifests and Rust implementation | Four planned manifests and existing crates | Preserved by this task | Verify byte identities against baseline |

The baseline commit supplies repository preimages. The final commit and its readback supply the applied file list and postimages. Publish only this scoped change, with the expected branch head and a non-force update. If the head changed, inspect and reconcile before retrying. An independent review must inspect concrete changes; a worker's test report alone is not the integration decision.

No Project schema/view/workflow, issue lifecycle, assignee, label, PR state, repository setting, release, tag, credential, host, or paid workload is changed by this plan. Repository research CI is the only workflow file amended. No new experiment or human session is claimed as executed.

## Record and projection cutover

The manual record format is available when its code, documentation, examples, and tests are integrated. Real accepted records begin in `harness/coordination/records/` with demonstration mode false; synthetic examples remain separate. No example is a live assignment, owner approval, result, or resource reservation.

Binding a GitHub Project is a later concrete operation. First obtain the actual Project identity and a permitted capability; inventory complete fields/items/views/workflows and relevant reports; record owner-specific API support; map existing vocabulary. Prepare exact preimages, ordered mutations, postimages, and reconciliation behavior before writing. The record link points to a committed canonical record, not a mutable latest comment.

Prototype one representative populated item before bulk projection. Read back every changed field/view/workflow and inspect the real phone/desktop presentation. Keep remaining unknowns visible. Source confirmation, canonical acceptance, projection confirmation, execution stop, and effect reconciliation remain distinct throughout cutover.

## Verification interpretation

Local tests can verify the checker and synthetic consistency cases. The current research manifests must remain planned and unrun unless an actual subsequent investigation changes them with evidence. CI results apply to their exact commit; a pending/queued run is reported as pending. Neither CI nor a JSON schema certifies the external evidence, actor identity, scientific conclusion, or operational performance of this protocol.
