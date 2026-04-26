from mathdevmcp.leandojo_spike import leandojo_import_smoke, leandojo_tiny_proof_spike


def test_leandojo_import_smoke_reports_core_classes():
    result = leandojo_import_smoke()

    assert result["metadata"] == {"schema_version": "1.0", "contract": "leandojo_spike_result"}
    assert result["status"] in {"available", "inconclusive"}
    if result["status"] == "available":
        assert result["details"]["has_dojo"] is True
        assert result["details"]["has_repo"] is True
        assert result["details"]["has_theorem"] is True


def test_leandojo_tiny_proof_spike_direct_checks_proof_artifact():
    result = leandojo_tiny_proof_spike()

    assert result["metadata"] == {"schema_version": "1.0", "contract": "leandojo_spike_result"}
    assert result["status"] in {"verified", "inconclusive"}
    if result["status"] == "verified":
        assert result["direct_check"]["status"] == "verified"
        assert result["tactic_trace"][0]["tactic"] == "exact Nat.add_comm a b"
    else:
        assert result["reason"]
