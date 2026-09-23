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

`deployments/studionet-release-2026-09-23.json` is the current StudioNet
evidence for source commit `7a9fb26a0b359136e0e164f2ba0281baedcbc1b2`.
Deployment and `review()` transactions are FINALIZED; both report successful
leader execution and MAJORITY_AGREE. The manifest records the deployed address,
transactions, frozen constructor inputs, final state, and checked Explorer
links. The source returned by StudioNet matches the release source after
normalizing line endings.

`deployments/studionet.json` is historical evidence for commit
`3f4aa3e3bfc62ae0a665b018042b3ed44309fb1c`; it is not the current deployment.
`deployments/studionet-candidate.json` is the preserved pre-deployment input
record, now superseded by the release manifest. The live Terraform example
compares version-pinned HashiCorp sources under a deployer-frozen MPL-2.0 to
BSL-1.1 materiality rule. Its v1.5.7 README identifies the MPL label but is not
the complete license, and both fetched sources are from the same repository.
This demonstrates one frozen-rule classification and route, not legal advice,
independent-publisher corroboration, every rule scenario, or semantic
prompt-injection resistance. See `docs/SECURITY_AUDIT.md` for residual limits.
