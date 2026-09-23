# GenLayer Portal submission

**Contribution type:** Builder → Intelligent Contracts
**Title:** Material Terms Change Guard

## Notes / Description (release candidate; do not paste until redeployed)

Material Terms Change Guard is an MIT-licensed GenLayer primitive for classifying agreement or policy amendments. Deployers freeze baseline terms, amendment, categories, adverse route, HTTPS evidence, minimum complete-source count, and deadline. Leader and validators independently classify each category as UNCHANGED, ADVERSE, BENEFICIAL, or UNCLEAR. Deterministic code derives status, route, and changed categories; validators compare the entire result. Missing, empty, invalid, oversized, or insufficient evidence yields UNRESOLVED / CAP_EXPOSURE. Material results are terminal; UNRESOLVED is retryable until the deadline. The candidate includes 29 direct tests, a pinned GenVM runner, audit, test matrix, and a version-pinned Terraform example. Existing StudioNet evidence is for an older source and does not prove this candidate. Direct tests do not prove prompt-injection resistance or live multi-validator behavior.

**Current live-proof status:** NOT READY. `deployments/studionet.json` is historical evidence for commit `3f4aa3e3bfc62ae0a665b018042b3ed44309fb1c`. A two-source, version-pinned constructor example is prepared in `deployments/studionet-candidate.json`; it is not deployed evidence. Deploy the patched source and these arguments on StudioNet, verify source identity and finality, then replace the live-proof paragraph and manifest.

## Evidence to add after publishing the candidate and collecting new live proof

1. GitHub Repository — https://github.com/JWattjr/material-terms-change-guard
2. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/contracts/material_terms_change_guard.py
3. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/tests/test_guard.py
4. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/docs/SECURITY_AUDIT.md
5. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/docs/TEST_MATRIX.md
6. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/deployments/studionet.json
7. GitHub File — `deployments/studionet-candidate.json` (candidate template; publish before submission)
8. GenLayer Explorer Contract (historical source only) — https://explorer-studio.genlayer.com/address/0x2C658385B6204d30be6eBA6CA3777dEf40cc78EE
9. GitHub File — Terraform v1.5.7 README (version-pinned baseline license label) — https://github.com/hashicorp/terraform/blob/v1.5.7/README.md
10. GitHub File — Terraform v1.6.0 LICENSE (version-pinned after-state license) — https://github.com/hashicorp/terraform/blob/v1.6.0/LICENSE

Historical resolution transaction hash: `0x30222f93a2892f0885027db96496a77cfe4c329092ff7a6cc43c12527ca1a8da`. Its direct Explorer URL could not be verified from this environment, so do not add an invented path.

## StudioNet release checklist

1. Use the prepared version-pinned source pair: v1.5.7 README (3.73 KB; identifies MPL 2.0) and v1.6.0 LICENSE (2.86 KB; identifies BSL 1.1). Both are from the same HashiCorp repository, so `min_sources=2` requires both version snapshots but is not independent-source corroboration. The complete v1.5.7 LICENSE is 15.6 KB, so the baseline term and market rule remain frozen deployer inputs. The candidate is a version comparison under that rule, not a legal opinion.
2. Commit and publish the patched source and tests. Record the exact commit and source hash; do not reuse the historical deployment as proof of it.
3. Deploy on **StudioNet only**, complete a permissionless `review()`, and verify both transactions are FINALIZED with successful execution and majority agreement. Read back the final state and compare it with the frozen constructor inputs.
4. Save a new manifest with address, release commit, constructor, transaction hashes, receipts, validator outcome, final state, and verified Explorer links. Then update the Portal text and evidence list.
