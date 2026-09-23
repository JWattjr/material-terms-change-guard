# Security and consensus audit: Material Terms Change Guard

Audit updated: 2026-09-23
Scope: contracts/material_terms_change_guard.py

This is an engineering audit, not formal verification, and not a financial or legal guarantee.

## Remediated findings

| ID | Severity | Finding | Remediation |
| --- | --- | --- | --- |
| MT-01 | High | The validator compared only `status`. `changed_rights` was written to state and exposed through `get_state()` unbound, so validators could agree on a verdict while persisting different accounts of which rights changed. | The validator requires whole-result equality with its own independent evaluation. |
| MT-02 | High | The LLM chose the verdict directly. | The LLM returns a per-category vector over the frozen categories; deterministic code derives status, route, and changed categories. |
| MT-03 | Medium | `changed_rights` accepted any label, and a source outage stored `SOURCES_UNAVAILABLE` as if it were a right. | Labels are restricted to the frozen categories; outages are reported through `source_coverage`. |
| MT-04 | Medium | `PAUSE_MINT` and `MIGRATE` were declared but unreachable. | The deployer freezes `adverse_route`; a confirmed adverse change takes it. |
| MT-05 | Medium | Resolution was owner-gated and never terminal, so a verdict could be re-run and flipped. | `review()` is permissionless over frozen inputs. Material verdicts are terminal; only `UNRESOLVED` can be retried. |
| MT-07 | Medium | One reachable source was enough to decide. | Frozen `min_sources`; fewer complete sources fail closed to `UNRESOLVED` without calling the LLM. |
| MT-08 | Medium | `UNRESOLVED` could be retried indefinitely. | Frozen `max_wait` deadline after which the current state is final; a never-reviewed amendment becomes `UNRESOLVED` / `CAP_EXPOSURE`. |
| MT-09 | Low | Baseline terms were unbounded and could bloat the prompt. | Baseline capped at 4000 serialized characters. |
| MT-06 | Low | Categories and sources were unbounded and not de-duplicated. | 1-12 unique category labels; 1-6 unique public HTTPS sources; bounded amendment and instrument text. |

## Controls

| Area | Control |
| --- | --- |
| Consensus | Whole-result equality between the leader and an independent validator evaluation. |
| Determinism | Status, route, and changed categories are pure functions of the bound vector and frozen policy. |
| Evidence | DNS-hosted HTTPS only; IP literals, explicit ports, local/internal names, userinfo, and whitespace are rejected. A source counts only for a nonempty, complete UTF-8 body of at most 7,000 bytes. |
| Prompt safety | Evidence is untrusted data; the model can only fill the frozen category keys. This bounds output shape, not semantic prompt-injection resistance. |
| Failure mode | Uncertainty, fetch errors, or fewer complete sources than `min_sources` become `UNRESOLVED` / `CAP_EXPOSURE`, never `CONTINUE`. |
| Lifecycle | Material verdicts are final. `UNRESOLVED` is retriable until the frozen `max_wait`, then final. |
| State | Inputs are snapshotted before the nondeterministic closures, which contain no `self`. |

## Residual risks

- Whole-result equality means validators that read an ambiguous amendment differently fail closed rather than settle. This is deliberate.
- Public webpages can change or disappear; use stable primary sources.
- HTTPS does not prove source authority; the deployer chooses official sources.
- DNS names can resolve to non-public addresses or change after deployment; the URL syntax check is not a network-layer SSRF guarantee.
- The historical deployment's single mutable license source and deployer-authored baseline do not prove historical before/after provenance. The prepared candidate fetches two version-pinned sources, but its baseline and materiality rule remain deployer-frozen.
- Mocked direct tests do not prove semantic prompt-injection resistance or independent live-validator correctness.
- Downstream protocols must wait for GenLayer finality before acting on a route.
- The StudioNet manifest records commit `3f4aa3e3bfc62ae0a665b018042b3ed44309fb1c`; it is historical relative to these uncommitted fixes.
