import json

import pytest

SRC = "contracts/material_terms_change_guard.py"
BASELINE = {"redemption_fee_bps": 10, "redemption_window": "T+1", "freeze_rights": "court order only"}
POLICY = {"material_categories": ["REDEMPTION_FEES", "REDEMPTION_WINDOW", "FREEZE_RIGHTS"], "adverse_route": "PAUSE_MINT"}
URLS = ["https://example.org/terms-v2"]


def _deploy(direct_deploy, policy=POLICY, urls=URLS):
    return direct_deploy(SRC, "usdx", "Terms v2 amendment", BASELINE, policy, urls)


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


@pytest.mark.parametrize("policy,urls,message", [
    ({"material_categories": []}, URLS, "1-12"),
    ({"material_categories": ["FEES", "fees"]}, URLS, "unique"),
    ({"material_categories": ["FEES"], "adverse_route": "LIQUIDATE"}, URLS, "adverse_route"),
    (POLICY, ["https://192.168.1.1/terms"], "public"),
    (POLICY, URLS + URLS, "unique"),
])
def test_constructor_rejections(direct_vm, direct_deploy, policy, urls, message):
    with direct_vm.expect_revert(message):
        _deploy(direct_deploy, policy=policy, urls=urls)
