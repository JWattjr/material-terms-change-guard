# Test matrix: Material Terms Change Guard

| Scenario | Expected behavior | Test |
| --- | --- | --- |
| All categories unchanged | `NO_MATERIAL_CHANGE` / `CONTINUE`; validator agrees | `test_no_material_change_continues_and_is_terminal` |
| Released, version-pinned Terraform example and frozen materiality rule | Both evidence URLs required; adverse category deterministically routes to `MIGRATE` | `test_released_studionet_example_runs_its_frozen_rule` |
| Repeat review after a terminal verdict | Verdict cannot flip; no new attempt recorded | `test_no_material_change_continues_and_is_terminal` |
| Any adverse category | `MATERIAL_ADVERSE_CHANGE`, frozen adverse route, changed categories listed | `test_adverse_change_takes_frozen_route_and_lists_categories` |
| Beneficial only | `MATERIAL_BENEFICIAL_CHANGE` / `CONTINUE` | `test_beneficial_only_continues` |
| Any unclear category | `UNRESOLVED` / `CAP_EXPOSURE`, stays retriable | `test_unclear_category_fails_closed_and_stays_retriable` |
| Omitted, invented, or invalid category labels | Normalized to the frozen allowlist; invalid values become `UNCLEAR` | `test_missing_and_invented_categories_are_normalized` |
| All sources unavailable | LLM not called; `UNRESOLVED` with coverage 0 | `test_all_sources_unavailable_skips_llm_and_fails_closed` |
| Empty, oversized, or invalid UTF-8 HTTP 200 body | Does not count as coverage; `UNRESOLVED` | `test_empty_oversized_or_invalid_evidence_is_not_counted` (4 cases) |
| Leader forges the category vector but keeps the same status | Validator rejects | `test_validator_rejects_divergent_category_vector_with_same_status` |
| Leader status inconsistent with its own vector | Validator rejects | `test_validator_rejects_status_inconsistent_with_vector` |
| Fewer complete sources than `min_sources` | `UNRESOLVED` / `CAP_EXPOSURE` without calling the LLM | `test_fewer_reachable_sources_than_min_sources_fails_closed` |
| `max_wait` passes on `UNRESOLVED` | State frozen as final | `test_max_wait_freezes_unresolved_state` |
| `max_wait` passes with no review | `UNRESOLVED`, final | `test_max_wait_without_review_is_unresolved` |
| Bad `min_sources`, `max_wait`, or oversized baseline | Constructor reverts | `test_constructor_rejects_bad_lifecycle_and_baseline` (5 cases) |
| Bad constructor input (categories, route, private/IPv6/ported/whitespace or duplicate URLs) | Constructor reverts | `test_constructor_rejections` (8 cases) |
| Finality | Downstream irreversible actions wait for GenLayer finality | Consumer responsibility |
