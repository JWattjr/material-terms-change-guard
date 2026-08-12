import json
def test_material_terms_consensus(direct_vm,direct_deploy):
    c=direct_deploy("contracts/material_terms_change_guard.py","asset",{"terms":"v1"},{"material_categories":["REDEMPTION_FEES"]},["https://example.org/terms"])
    direct_vm.mock_web(r".*",{"status":200,"body":"terms"});direct_vm.mock_llm(r".*",json.dumps({"status":"NO_MATERIAL_CHANGE","route":"CONTINUE","changed_rights":[]}))
    assert c.review()["route"]=="CONTINUE" and direct_vm.run_validator()
