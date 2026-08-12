# GenLayer Portal submission

**Contribution type:** Builder â†’ Intelligent Contracts  
**Title:** Material Terms Change Guard

## Notes / Description

Built an MIT-licensed, standalone Material Terms Change Guard, a reusable GenLayer
Intelligent Contract that compares official current terms with an immutable stablecoin terms baseline.. The constructor freezes
bounded policy inputs and public HTTPS evidence sources. The leader and
validators independently evaluate the same material through a custom
equivalence function that compares the substantive structured decisionâ€”
NO_MATERIAL_CHANGE, MATERIAL_ADVERSE_CHANGE, MATERIAL_BENEFICIAL_CHANGE, or UNRESOLVEDâ€”rather than merely validating output shape. The accepted
decision continues, caps, pauses, or migrates protocol exposure. Local/private evidence targets, malformed input,
source failure, ambiguity, model-output errors, unauthorized calls, and
validator disagreement fail closed. The repository includes pinned GenVM
source, direct consensus tests, a security audit, test matrix, and StudioNet /
Bradbury deployment manifests. It is a composable policy primitive and does
not custody funds or claim legal/financial authority.

## Evidence to add

1. GitHub Repository â€” https://github.com/JWattjr/material-terms-change-guard
2. GitHub File â€” https://github.com/JWattjr/material-terms-change-guard/blob/main/contracts/material_terms_change_guard.py
3. GitHub File â€” https://github.com/JWattjr/material-terms-change-guard/blob/main/docs/SECURITY_AUDIT.md
4. GitHub File â€” https://github.com/JWattjr/material-terms-change-guard/blob/main/docs/TEST_MATRIX.md
5. GitHub File â€” https://github.com/JWattjr/material-terms-change-guard/blob/main/deployments/studionet.json
6. GitHub File â€” https://github.com/JWattjr/material-terms-change-guard/blob/main/deployments/bradbury.json
7. GenLayer Explorer Contract â€” add the final Bradbury address from deployments/bradbury.json
