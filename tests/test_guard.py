import json
from pathlib import Path

import pytest

SRC = "contracts/material_terms_change_guard.py"
BASELINE = {"redemption_fee_bps": 10, "redemption_window": "T+1", "freeze_rights": "court order only"}
POLICY = {"material_categories": ["REDEMPTION_FEES", "REDEMPTION_WINDOW", "FREEZE_RIGHTS"], "adverse_route": "PAUSE_MINT"}
URLS = ["https://example.org/terms-v2"]


MAX_WAIT = "2099-01-01T00:00:00Z"
ALL_UNCHANGED = {"REDEMPTION_FEES": "UNCHANGED", "REDEMPTION_WINDOW": "UNCHANGED", "FREEZE_RIGHTS": "UNCHANGED"}


def _deploy(direct_deploy, policy=POLICY, urls=URLS, min_sources=1, max_wait=MAX_WAIT, baseline=BASELINE):
    return direct_deploy(SRC, "usdx", "Terms v2 amendment", baseline, policy, urls, min_sources, max_wait)


def _mock(direct_vm, states, status=200):
    direct_vm.mock_web(r".*", {"status": status, "body": "amended terms"})
    direct_vm.mock_llm(r".*", json.dumps({"category_states": states}))


def test_no_material_change_continues_and_is_terminal(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, {"REDEMPTION_FEES": "UNCHANGED", "REDEMPTION_WINDOW": "UNCHANGED", "FREEZE_RIGHTS": "UNCHANGED"})
    result = c.review()
    assert result["status"] == "NO_MATERIAL_CHANGE" and result["route"] == "CONTINUE"
    assert direct_vm.run_validator()
    # Terminal: a later review cannot flip the verdict.
    direct_vm.clear_mocks()
    _mock(direct_vm, {"REDEMPTION_FEES": "ADVERSE", "REDEMPTION_WINDOW": "UNCHANGED", "FREEZE_RIGHTS": "UNCHANGED"})
    assert c.review()["status"] == "NO_MATERIAL_CHANGE"
    assert c.get_state()["attempts"] == 1


def test_released_studionet_example_runs_its_frozen_rule(direct_vm, direct_deploy):
    release = json.loads(Path("deployments/studionet-release-2026-09-23.json").read_text(encoding="utf-8"))
    assert release["release_status"] == "STUDIONET_DEPLOYED_AND_VERIFIED"
    assert release["source_file"] == SRC
    c = direct_deploy(SRC, *release["constructor_args"])
    direct_vm.mock_web(r"v1\.5\.7/README\.md", {"status": 200, "body": "License: Mozilla Public License v2.0"})
    direct_vm.mock_web(r"v1\.6\.0/LICENSE", {"status": 200, "body": "Business Source License 1.1; hosted competitive offering restriction"})
    direct_vm.mock_llm(r".*", json.dumps({"category_states": {"COMPETITIVE_PRODUCTION_USE": "ADVERSE"}}))
    result = c.review()
    assert result["status"] == "MATERIAL_ADVERSE_CHANGE"
    assert result["route"] == "MIGRATE"
    assert result["source_coverage"] == 2
    assert direct_vm.run_validator()


def test_adverse_change_takes_frozen_route_and_lists_categories(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, {"REDEMPTION_FEES": "ADVERSE", "REDEMPTION_WINDOW": "BENEFICIAL", "FREEZE_RIGHTS": "UNCHANGED"})
    result = c.review()
    assert result["status"] == "MATERIAL_ADVERSE_CHANGE"
    assert result["route"] == "PAUSE_MINT"
    assert result["changed_rights"] == ["REDEMPTION_FEES", "REDEMPTION_WINDOW"]
    assert c.get_state()["category_states"]["FREEZE_RIGHTS"] == "UNCHANGED"


def test_beneficial_only_continues(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, {"REDEMPTION_FEES": "BENEFICIAL", "REDEMPTION_WINDOW": "UNCHANGED", "FREEZE_RIGHTS": "UNCHANGED"})
    result = c.review()
    assert result["status"] == "MATERIAL_BENEFICIAL_CHANGE" and result["route"] == "CONTINUE"


def test_unclear_category_fails_closed_and_stays_retriable(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, {"REDEMPTION_FEES": "UNCLEAR", "REDEMPTION_WINDOW": "UNCHANGED", "FREEZE_RIGHTS": "UNCHANGED"})
    assert c.review()["status"] == "UNRESOLVED"
    assert c.get_state()["route"] == "CAP_EXPOSURE" and not c.get_state()["terminal"]


def test_missing_and_invented_categories_are_normalized(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    # FREEZE_RIGHTS omitted, a label invented, a state value invalid.
    _mock(direct_vm, {"REDEMPTION_FEES": "UNCHANGED", "REDEMPTION_WINDOW": "WORSE", "INVENTED": "ADVERSE"})
    result = c.review()
    assert set(result["category_states"]) == {"FREEZE_RIGHTS", "REDEMPTION_FEES", "REDEMPTION_WINDOW"}
    assert result["category_states"]["REDEMPTION_WINDOW"] == "UNCLEAR"
    assert result["status"] == "UNRESOLVED"


def test_all_sources_unavailable_skips_llm_and_fails_closed(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, {"REDEMPTION_FEES": "ADVERSE"}, status=503)
    result = c.review()
    assert result["status"] == "UNRESOLVED" and result["source_coverage"] == 0
    assert result["changed_rights"] == []


@pytest.mark.parametrize("body", ["", " ", "x" * 7001, b"\xff"])
def test_empty_oversized_or_invalid_evidence_is_not_counted(direct_vm, direct_deploy, body):
    c = _deploy(direct_deploy)
    direct_vm.mock_web(r".*", {"status": 200, "body": body})
    direct_vm.mock_llm(r".*", json.dumps({"category_states": ALL_UNCHANGED}))
    result = c.review()
    assert result["status"] == "UNRESOLVED" and result["source_coverage"] == 0
    assert direct_vm.run_validator()


def test_validator_rejects_divergent_category_vector_with_same_status(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, {"REDEMPTION_FEES": "ADVERSE", "REDEMPTION_WINDOW": "UNCHANGED", "FREEZE_RIGHTS": "UNCHANGED"})
    honest = c.review()
    # Same status and route, different account of which rights changed.
    forged = dict(honest, category_states=dict(honest["category_states"], REDEMPTION_FEES="UNCHANGED", FREEZE_RIGHTS="ADVERSE"),
                  changed_rights=["FREEZE_RIGHTS"])
    assert not direct_vm.run_validator(leader_result=forged)


def test_validator_rejects_status_inconsistent_with_vector(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, {"REDEMPTION_FEES": "ADVERSE", "REDEMPTION_WINDOW": "UNCHANGED", "FREEZE_RIGHTS": "UNCHANGED"})
    honest = c.review()
    assert not direct_vm.run_validator(leader_result=dict(honest, status="NO_MATERIAL_CHANGE", route="CONTINUE"))


def test_fewer_reachable_sources_than_min_sources_fails_closed(direct_vm, direct_deploy):
    c = _deploy(direct_deploy, urls=["https://example.org/a", "https://example.net/b"], min_sources=2)
    direct_vm.mock_web(r"example\.org", {"status": 200, "body": "amended terms"})
    direct_vm.mock_web(r"example\.net", {"status": 503, "body": "down"})
    direct_vm.mock_llm(r".*", json.dumps({"category_states": ALL_UNCHANGED}))
    result = c.review()
    assert result["status"] == "UNRESOLVED" and result["route"] == "CAP_EXPOSURE" and result["source_coverage"] == 1


def test_max_wait_freezes_unresolved_state(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, dict(ALL_UNCHANGED, FREEZE_RIGHTS="UNCLEAR"))
    assert c.review()["status"] == "UNRESOLVED"
    direct_vm.warp("2100-01-01T00:00:00Z")
    direct_vm.clear_mocks()
    _mock(direct_vm, ALL_UNCHANGED)
    state = c.review()
    assert state["status"] == "UNRESOLVED" and state["route"] == "CAP_EXPOSURE" and state["terminal"]
    assert state["attempts"] == 1


def test_max_wait_without_review_is_unresolved(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    direct_vm.warp("2100-01-01T00:00:00Z")
    state = c.review()
    assert state["status"] == "UNRESOLVED" and state["terminal"] and state["attempts"] == 0


@pytest.mark.parametrize("kwargs,message", [
    ({"min_sources": 0}, "min_sources"),
    ({"min_sources": 2}, "min_sources"),
    ({"max_wait": "2000-01-01T00:00:00Z"}, "future"),
    ({"max_wait": "2099-01-01T00:00:00"}, "timezone"),
    ({"baseline": {"terms": "x" * 4001}}, "4000"),
])
def test_constructor_rejects_bad_lifecycle_and_baseline(direct_vm, direct_deploy, kwargs, message):
    with direct_vm.expect_revert(message):
        _deploy(direct_deploy, **kwargs)


@pytest.mark.parametrize("policy,urls,message", [
    ({"material_categories": []}, URLS, "1-12"),
    ({"material_categories": ["FEES", "fees"]}, URLS, "unique"),
    ({"material_categories": ["FEES"], "adverse_route": "LIQUIDATE"}, URLS, "adverse_route"),
    (POLICY, ["https://192.168.1.1/terms"], "public"),
    (POLICY, ["https://[::1]/terms"], "public"),
    (POLICY, ["https://example.org:443/terms"], "public"),
    (POLICY, ["https://example.org /terms"], "public"),
    (POLICY, URLS + URLS, "unique"),
])
def test_constructor_rejections(direct_vm, direct_deploy, policy, urls, message):
    with direct_vm.expect_revert(message):
        _deploy(direct_deploy, policy=policy, urls=urls)
