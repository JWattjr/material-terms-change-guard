# GenLayer Portal submission

**Contribution type:** Builder → Intelligent Contracts
**Title:** Material Terms Change Guard

## Notes / Description (draft; public-access blocker)

**Access blocker:** The GitHub repository is currently PRIVATE. Unauthenticated checks returned HTTP 404 for the repository and every GitHub evidence file linked below. The StudioNet Explorer pages are public and verified, but Portal reviewers cannot inspect the source, tests, audit, or manifest until the repository is made public or equivalent public evidence is provided. Do not submit while this blocker remains.

Material Terms Change Guard is an MIT-licensed GenLayer primitive for classifying agreement or policy amendments. Deployers freeze the baseline, amendment, categories, route, HTTPS sources, minimum source coverage, and deadline. Leader and validators independently classify each frozen category; deterministic code derives the outcome and the validators compare the full result. In the StudioNet demonstration, the version-pinned Terraform v1.5.7 README and v1.6.0 license produced `MATERIAL_ADVERSE_CHANGE` / `MIGRATE` under the frozen rule; both sources were available. The deployment and resolution finalized with successful leader execution and majority agreement. This demonstrates one rule-driven case only: it is not legal advice, does not prove every edge case, and does not guarantee semantic prompt-injection resistance. The repository includes 29 focused tests, a pinned GenVM runner, security audit, and test matrix.

**Current live proof:** StudioNet contract [`0x83d2FF1206cdf5243E6353DdE4bCbF2D0B42eDF8`](https://explorer-studio.genlayer.com/address/0x83d2FF1206cdf5243E6353DdE4bCbF2D0B42eDF8), source commit `7a9fb26a0b359136e0e164f2ba0281baedcbc1b2`, source SHA-256 `6c15d5a6db7eddb003d4a771d5f1ae08043474f91b489537db50dad1b38b88e8`. Deployment transaction [`0x99e030ebb30c0f5c3b08b3fa7cdfb660eddc326eeab65426e25c091186b7e33b`](https://explorer-studio.genlayer.com/tx/0x99e030ebb30c0f5c3b08b3fa7cdfb660eddc326eeab65426e25c091186b7e33b) and resolution transaction [`0x7c599b51459501f00bfb91491d793627afc42bb5f93847987445ff4e728bee05`](https://explorer-studio.genlayer.com/tx/0x7c599b51459501f00bfb91491d793627afc42bb5f93847987445ff4e728bee05) are FINALIZED. The resolution is `MAJORITY_AGREE`, not unanimous: 3 AGREE and 2 IDLE validator votes were recorded; a validator execution was canceled after quorum. `get_state()` reads back terminal status `MATERIAL_ADVERSE_CHANGE`, route `MIGRATE`, category `COMPETITIVE_PRODUCTION_USE: ADVERSE`, source coverage 2, and one attempt. See [`deployments/studionet-release-2026-09-23.json`](deployments/studionet-release-2026-09-23.json) for complete receipts and inputs.

## Evidence links

1. GitHub Repository — https://github.com/JWattjr/material-terms-change-guard
2. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/contracts/material_terms_change_guard.py
3. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/tests/test_guard.py
4. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/docs/SECURITY_AUDIT.md
5. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/docs/TEST_MATRIX.md
6. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/deployments/studionet-release-2026-09-23.json
7. GenLayer Explorer Contract — https://explorer-studio.genlayer.com/address/0x83d2FF1206cdf5243E6353DdE4bCbF2D0B42eDF8
8. GenLayer Explorer Deployment Transaction — https://explorer-studio.genlayer.com/tx/0x99e030ebb30c0f5c3b08b3fa7cdfb660eddc326eeab65426e25c091186b7e33b
9. GenLayer Explorer Resolution Transaction — https://explorer-studio.genlayer.com/tx/0x7c599b51459501f00bfb91491d793627afc42bb5f93847987445ff4e728bee05
10. GitHub File — Terraform v1.5.7 README (version-pinned baseline license label) — https://github.com/hashicorp/terraform/blob/v1.5.7/README.md
11. GitHub File — Terraform v1.6.0 LICENSE (version-pinned after-state license) — https://github.com/hashicorp/terraform/blob/v1.6.0/LICENSE

## Scope and limitations

The evidence is a successful basic demonstration of a frozen-rule, permissionless classification using two version-pinned sources from the same repository. The v1.5.7 README identifies MPL-2.0 but is not the complete license; the baseline label and materiality rule are deployer-frozen inputs, not a legal determination. The live example does not exercise complex exceptions, conflicting-rule handling, postponement recovery, or prompt-injection resistance. Local tests cover additional branches, but mocked direct tests do not establish live multi-validator behavior for those cases. `deployments/studionet.json` and the older contract address are historical only; this submission's current evidence is StudioNet.
