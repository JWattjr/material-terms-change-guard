# Material Terms Change Guard

Decides whether a proposed amendment materially changes an agreement or policy,
and routes protocol exposure accordingly.

## How it decides

The deployer freezes the baseline terms, a short description of the amendment,
1-12 material categories, the route to take on an adverse change
(`CAP_EXPOSURE`, `PAUSE_MINT`, or `MIGRATE`), 1-6 public HTTPS evidence URLs,
`min_sources` (how many must return nonempty, complete UTF-8 evidence to decide),
and a `max_wait` deadline. Sources must use DNS-hosted HTTPS URLs; IP literals
and explicit ports are rejected. A fetch error, non-200 response, empty body,
invalid UTF-8, or body over 7,000 bytes does not count toward coverage.

1. Leader and validators each fetch the evidence and classify **every frozen
   category** as `UNCHANGED`, `ADVERSE`, `BENEFICIAL`, or `UNCLEAR`. Labels
   outside the frozen list are dropped; missing or invalid values become `UNCLEAR`.
2. Deterministic code derives the verdict from that vector. The LLM never picks it:
   - any `UNCLEAR`, or fewer than `min_sources` complete sources → `UNRESOLVED`, route `CAP_EXPOSURE`
   - any `ADVERSE` → `MATERIAL_ADVERSE_CHANGE`, route = the frozen adverse route
   - only `BENEFICIAL` → `MATERIAL_BENEFICIAL_CHANGE`, route `CONTINUE`
   - all `UNCHANGED` → `NO_MATERIAL_CHANGE`, route `CONTINUE`
3. The validator requires the **entire result** to match its own independent
   evaluation: status, route, the full category vector, changed categories, and
   source coverage. This binds the stored result but does not guarantee that
   independently running LLMs interpret every document correctly.

The three material verdicts are terminal and cannot be flipped by a later review.
`UNRESOLVED` stays retriable until `max_wait`; after it, the current state becomes
final (an amendment never reviewed becomes `UNRESOLVED` with exposure capped). `review()` is permissionless because every input
is frozen. The contract holds no funds.

## Verify

    python -m genvm_linter.cli lint contracts/material_terms_change_guard.py --json
    python -m pytest tests -v

See docs/SECURITY_AUDIT.md and docs/TEST_MATRIX.md.

## Deployment evidence scope

`deployments/studionet.json` records a finalized StudioNet result for source
commit `3f4aa3e3bfc62ae0a665b018042b3ed44309fb1c`. The local source now has
additional evidence-validation fixes and is **not** the source at that address.
`deployments/studionet-candidate.json` prepares a two-source, version-pinned
example using the v1.5.7 README's MPL label and the v1.6.0 BSL license. The
v1.5.7 README is not the full license; the baseline and classification rule are
frozen deployer inputs. The historical one-source `main/LICENSE` deployment
does not prove this example, all rule scenarios, or semantic prompt-injection
resistance. Redeploy this exact source and finalize a new resolution before
presenting it as current live proof.
