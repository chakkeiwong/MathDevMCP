from pathlib import Path
import zipfile

from mathdevmcp.release_artifacts import build_release_manifest, write_release_manifest


def _wheel(path: Path) -> Path:
    wheel = path / "mathdevmcp-0.1.0-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("mathdevmcp/__init__.py", "")
        archive.writestr(
            "mathdevmcp-0.1.0.dist-info/METADATA",
            "Metadata-Version: 2.1\nName: mathdevmcp\nVersion: 0.1.0\nRequires-Python: >=3.11\n",
        )
    return wheel


def test_release_manifest_binds_wheel_and_declines_unlocked_claim(tmp_path: Path) -> None:
    wheel = _wheel(tmp_path)
    lock = tmp_path / "constraints.txt"
    lock.write_text("mathdevmcp==0.1.0\n", encoding="utf-8")

    manifest = build_release_manifest(tmp_path, wheel, dependency_lock=lock, test_summary={"status": "passed"})

    assert manifest["schema_version"] == "mathdevmcp-release-manifest@1"
    assert manifest["wheel"]["sha256"]
    assert manifest["wheel"]["metadata"] == {"Name": "mathdevmcp", "Version": "0.1.0", "Requires-Python": ">=3.11"}
    assert manifest["dependency_lock"]["status"] == "supplied"
    assert manifest["test_summary"] == {"status": "passed"}
    assert manifest["test_evidence_binding"]["status"] == "unbound_caller_supplied"
    assert manifest["claims"]["test_evidence_bound"] is False
    assert manifest["claims"]["mathematical_correctness"] == "not_evaluated"


def test_release_manifest_binds_only_a_real_passed_evidence_artifact(tmp_path: Path, monkeypatch) -> None:
    wheel = _wheel(tmp_path)
    evidence = tmp_path / "tests.json"
    evidence.write_text("{\"status\":\"passed\"}\n", encoding="utf-8")
    import hashlib
    import subprocess
    import mathdevmcp.release_artifacts as release_artifacts

    commit = "abc123"
    original_run = release_artifacts.subprocess.run

    def fake_run(command, **kwargs):
        if command[-1] == "--short":
            return subprocess.CompletedProcess(command, 0, "", "")
        if command[-2:] == ["rev-parse", "HEAD"]:
            return subprocess.CompletedProcess(command, 0, commit + "\n", "")
        return original_run(command, **kwargs)

    monkeypatch.setattr(release_artifacts.subprocess, "run", fake_run)
    wheel_sha256 = hashlib.sha256(wheel.read_bytes()).hexdigest()
    summary = {
        "status": "passed",
        "artifact_path": str(evidence),
        "artifact_sha256": hashlib.sha256(evidence.read_bytes()).hexdigest(),
        "git_commit": commit,
        "wheel_sha256": wheel_sha256,
    }
    manifest = build_release_manifest(tmp_path, wheel, test_summary=summary)
    assert manifest["test_evidence_binding"]["status"] == "verified"
    assert manifest["claims"]["test_evidence_bound"] is True


def test_release_manifest_marks_missing_lock_without_overclaiming(tmp_path: Path) -> None:
    wheel = _wheel(tmp_path)
    manifest = build_release_manifest(tmp_path, wheel)

    assert manifest["dependency_lock"] == {"status": "not_supplied", "sha256": None, "path": None}
    assert manifest["claims"]["dependency_reproducibility"] == "not_claimed_without_lock"


def test_release_manifest_writer_is_canonical_json(tmp_path: Path) -> None:
    wheel = _wheel(tmp_path)
    output = tmp_path / "nested" / "manifest.json"
    write_release_manifest(build_release_manifest(tmp_path, wheel), output)

    assert output.is_file()
    assert output.read_text(encoding="utf-8").endswith("\n")


def test_release_manifest_writer_rejects_different_overwrite(tmp_path: Path) -> None:
    output = tmp_path / "manifest.json"
    write_release_manifest({"x": 1}, output)
    try:
        write_release_manifest({"x": 2}, output)
    except ValueError as exc:
        assert "collision" in str(exc)
    else:
        raise AssertionError("release manifest overwrite was accepted")
