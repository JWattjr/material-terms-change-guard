# Material Terms Change Guard

Decides whether a proposed amendment materially changes an agreement or policy,
and routes protocol exposure accordingly.

## How it decides

The deployer freezes the baseline terms, a short description of the amendment,
1-12 material categories, the route to take on an adverse change
(`CAP_EXPOSURE`, `PAUSE_MINT`, or `MIGRATE`), and 1-6 public HTTPS evidence URLs.

1. Leader and validators each fetch the evidence and classify **every frozen
   category** as `UNCHANGED`, `ADVERSE`, `BENEFICIAL`, or `UNCLEAR`. Labels
   outside the frozen list are dropped; missing or invalid values become `UNCLEAR`.
2. Deterministic code derives the verdict from that vector. The LLM never picks it:
   - any `UNCLEAR`, or no source reachable → `UNRESOLVED`, route `CAP_EXPOSURE`
   - any `ADVERSE` → `MATERIAL_ADVERSE_CHANGE`, route = the frozen adverse route
   - only `BENEFICIAL` → `MATERIAL_BENEFICIAL_CHANGE`, route `CONTINUE`
   - all `UNCHANGED` → `NO_MATERIAL_CHANGE`, route `CONTINUE`
3. The validator requires the **entire result** to match its own independent
   evaluation: status, route, the full category vector, changed categories, and
   source coverage. Nothing reaches state without consensus.

The three material verdicts are terminal and cannot be flipped by a later review.
`UNRESOLVED` stays retriable. `review()` is permissionless because every input
is frozen. The contract holds no funds.

## Verify

    python -m genvm_linter.cli lint contracts/material_terms_change_guard.py --json
    python -m pytest tests -v

See docs/SECURITY_AUDIT.md and docs/TEST_MATRIX.md.
