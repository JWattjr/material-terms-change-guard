# Material Terms Change Guard

Compares official current terms with an immutable stablecoin terms baseline.

## GenLayer-native decision

The contract makes the consensus-critical decision: **NO_MATERIAL_CHANGE, MATERIAL_ADVERSE_CHANGE, MATERIAL_BENEFICIAL_CHANGE, or UNRESOLVED**. It
freezes bounded inputs and approved public evidence sources. The leader and
validators independently fetch/evaluate that evidence and compare the compact
decision fields using a custom equivalence function. After consensus, the
calling protocol deterministically continues, caps, pauses, or migrates protocol exposure.

The contract fails closed when evidence is unavailable, ambiguous, or
validator consensus does not support the same substantive result. It does not
use a frontend answer, a single backend, or format-only validation.

## Verify

Run: python -m genvm_linter.cli lint contracts/material_terms_change_guard.py --json
Run: python -m pytest tests -v

See docs/SECURITY_AUDIT.md, docs/TEST_MATRIX.md, and PORTAL_SUBMISSION.md.
