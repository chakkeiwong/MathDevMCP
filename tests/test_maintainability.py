from pathlib import Path

from mathdevmcp.maintainability import maintainability_report


ROOT = Path(__file__).resolve().parent.parent


def test_maintainability_stays_within_reviewed_handoff_baseline() -> None:
    report = maintainability_report(ROOT)

    assert report["status"] == "consistent", report["findings"]
    assert report["ratchet_status"] == "consistent"
    assert report["target_status"] == "debt_present"
    assert report["target_hotspot_count"] == len(report["target_hotspots"])
    assert report["target_hotspot_count"] > 0
    assert "establishes mathematical" in report["interpretation"]
    assert report["metadata"] == {"schema_version": "1.0", "contract": "maintainability_report"}
    assert report["import_cycles"] == []
    assert report["largest_modules"][0]["line_count"] <= report["baseline"]["max_module_lines"]
    assert report["largest_functions"][0]["line_count"] <= report["baseline"]["max_function_lines"]
    assert report["highest_import_fanout"][0]["import_fanout"] <= report["baseline"]["max_import_fanout"]
    assert report["highest_complexity_functions"][0]["estimated_complexity"] <= report["baseline"]["max_estimated_complexity"]
    assert report["complexity_20_count"] <= report["baseline"]["max_complexity_20_count"]
    assert report["highest_import_fanout"][0]["path"].endswith("cli.py")


def test_maintainability_targets_are_stricter_than_historical_ratchet() -> None:
    report = maintainability_report(ROOT)

    for key in ("max_module_lines", "max_function_lines", "max_import_fanout", "max_estimated_complexity"):
        assert report["targets"][key] < report["baseline"][key]
