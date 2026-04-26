from mathdevmcp.operation_consistency import compare_operations, extract_operations


def test_extract_operations_detects_logdet_and_solve():
    ops = extract_operations("compute logdet using solve and trace")

    assert "logdet" in ops
    assert "inverse_or_solve" in ops
    assert "trace" in ops


def test_compare_operations_detects_missing_logdet():
    result = compare_operations("likelihood has logdet and quadratic form", "return quadratic", required_operations=["logdet", "quadratic_form"])

    assert result["status"] == "mismatch"
    assert result["missing_operations"] == ["logdet"]


def test_compare_operations_passes_correct_fixture():
    result = compare_operations("likelihood has logdet", "sign, logdet = slogdet(S)", required_operations=["logdet"])

    assert result["status"] == "consistent"
    assert result["missing_operations"] == []
