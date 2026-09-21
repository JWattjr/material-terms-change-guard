# GenLayer Portal submission

**Contribution type:** Builder → Intelligent Contracts
**Title:** Material Terms Change Guard

## Notes / Description

Built and deployed an MIT-licensed Material Terms Change Guard: a reusable GenLayer primitive that decides whether a proposed amendment materially changes an agreement or policy, and routes protocol exposure. The constructor freezes baseline terms, the amendment, 1-12 material categories, an adverse-change route (CAP_EXPOSURE, PAUSE_MINT, or MIGRATE), and public HTTPS evidence. Leader and validators each classify every frozen category as UNCHANGED, ADVERSE, BENEFICIAL, or UNCLEAR; labels outside the frozen list are dropped. The LLM never picks the verdict: deterministic code derives status, route, and changed categories from the vector. The custom validator requires whole-result equality with its own independent evaluation, so the full category vector, verdict, route, and source coverage are all bound and nothing reaches state unverified. Uncertainty and source outages fail closed to UNRESOLVED / CAP_EXPOSURE. Material verdicts are terminal and cannot be flipped; review is permissionless over frozen inputs. Includes pinned GenVM source, 13 direct tests (including forged-vector and inconsistent-status leaders), a security audit, a test matrix, and StudioNet/Bradbury deployment records. It is a decision primitive and holds no funds.

## Evidence to add

1. GitHub Repository — https://github.com/JWattjr/material-terms-change-guard
2. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/contracts/material_terms_change_guard.py
3. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/tests/test_guard.py
4. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/docs/SECURITY_AUDIT.md
5. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/docs/TEST_MATRIX.md
6. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/deployments/studionet.json
7. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/deployments/bradbury.json
8. GenLayer Explorer Contract — the final Bradbury address from deployments/bradbury.json
