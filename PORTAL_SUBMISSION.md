# GenLayer Portal submission

**Contribution type:** Builder → Intelligent Contracts
**Title:** Material Terms Change Guard

## Notes / Description

Built and deployed an MIT-licensed Material Terms Change Guard: a reusable GenLayer primitive that decides whether a proposed amendment materially changes an agreement or policy, and routes protocol exposure. The constructor freezes baseline terms, the amendment, 1-12 material categories, an adverse-change route (CAP_EXPOSURE, PAUSE_MINT, or MIGRATE), and public HTTPS evidence. Leader and validators each classify every frozen category as UNCHANGED, ADVERSE, BENEFICIAL, or UNCLEAR; labels outside the frozen list are dropped. The LLM never picks the verdict: deterministic code derives status, route, and changed categories from the vector. The custom validator requires whole-result equality with its own independent evaluation, so the full category vector, verdict, route, and source coverage are all bound and nothing reaches state unverified. Uncertainty and source outages fail closed to UNRESOLVED / CAP_EXPOSURE. Material verdicts are terminal and cannot be flipped; review is permissionless over frozen inputs. Includes pinned GenVM source, 13 direct tests (including forged-vector and inconsistent-status leaders), a security audit, a test matrix, and a finalized StudioNet deployment with a live consensus result: judged against Terraform's published license, validators agreed the 2023 MPL-2.0 to BUSL-1.1 relicensing is an ADVERSE change to competitive production use with source access UNCHANGED, and the guard resolved MATERIAL_ADVERSE_CHANGE / MIGRATE. It is a decision primitive and holds no funds.

## Evidence to add

1. GitHub Repository — https://github.com/JWattjr/material-terms-change-guard
2. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/contracts/material_terms_change_guard.py
3. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/tests/test_guard.py
4. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/docs/SECURITY_AUDIT.md
5. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/docs/TEST_MATRIX.md
6. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/deployments/studionet.json
7. GenLayer Explorer Contract — https://explorer-studio.genlayer.com/address/0x4Eb5DdeE95B841105A0C5Ed7f1167EC61e346297
