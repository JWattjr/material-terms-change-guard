# GenLayer Portal submission

**Contribution type:** Builder → Intelligent Contracts  
**Title:** Material Terms Change Guard

## Notes / Description

Built an MIT-licensed Material Terms Change Guard: a reusable GenLayer primitive comparing published current terms to an immutable stablecoin terms baseline. It freezes material-change categories and public HTTPS evidence. Leader and validators independently assess the material; custom equivalence compares the substantive status, not output shape. The accepted status can continue, cap, pause, or migrate protocol exposure. Private/malformed evidence, source failures, ambiguity, unauthorized callers, and validator disagreement fail closed. Includes pinned GenVM source, direct consensus tests, security audit, test matrix, StudioNet and Bradbury evidence.

## Evidence to add

1. GitHub Repository — https://github.com/JWattjr/material-terms-change-guard
2. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/contracts/material_terms_change_guard.py
3. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/docs/SECURITY_AUDIT.md
4. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/docs/TEST_MATRIX.md
5. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/deployments/studionet.json
6. GitHub File — https://github.com/JWattjr/material-terms-change-guard/blob/main/deployments/bradbury.json
7. GenLayer Explorer Contract — add the final Bradbury address from deployments/bradbury.json
