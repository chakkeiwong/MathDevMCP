"""Release artifact identity and manifest helpers.

This module records engineering identity for a wheel that has actually been
built.  It does not certify mathematical correctness or dependency
reproducibility when no lock artifact was supplied.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

from .artifact_storage import write_bytes_no_replace

def build_release_manifest(
    root: str | Path,
    wheel: str | Path,
    *,
    dependency_lock: str | Path | None = None,
    test_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a manifest binding a wheel digest to the source checkout."""

    root_path = Path(root).resolve()
    wheel_path = Path(wheel).resolve()
    raw = wheel_path.read_bytes()
    lock_path = Path(dependency_lock).resolve() if dependency_lock else None
    status = subprocess.run(
        ["git", "-C", str(root_path), "status", "--short"],
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    commit = subprocess.run(
        ["git", "-C", str(root_path), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    metadata = _wheel_metadata(wheel_path)
    supplied_tests = test_summary or {"status": "not_recorded"}
    test_binding = {
        "status": "verified"
        if isinstance(supplied_tests, dict)
        and supplied_tests.get("git_commit") == commit.stdout.strip()
        and supplied_tests.get("wheel_sha256") == hashlib.sha256(raw).hexdigest()
        else "unbound_caller_supplied"
    }
    manifest: dict[str, Any] = {
        "schema_version": "mathdevmcp-release-manifest@1",
        "source": {
            "commit": commit.stdout.strip() or "unknown",
            "dirty": bool(status.stdout.strip()),
            "dirty_path_count": len(status.stdout.splitlines()),
        },
        "wheel": {
            "filename": wheel_path.name,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "byte_count": len(raw),
            "metadata": metadata,
        },
        "environment": {
            "python": sys.version.split()[0],
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "dependency_lock": _lock_identity(lock_path),
        "test_summary": supplied_tests,
        "test_evidence_binding": test_binding,
        "claims": {
            "wheel_identity_bound": True,
            "test_evidence_bound": test_binding["status"] == "verified",
            "dependency_reproducibility": "not_claimed_without_lock",
            "mathematical_correctness": "not_evaluated",
        },
    }
    return manifest


def write_release_manifest(manifest: dict[str, Any], output: str | Path) -> Path:
    """Write a canonical JSON manifest and return its path."""

    output_path = Path(output)
    payload = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    write_bytes_no_replace(output_path, payload)
    return output_path


def _lock_identity(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"status": "not_supplied", "sha256": None, "path": None}
    if not path.is_file():
        return {"status": "missing", "sha256": None, "path": path.name}
    raw = path.read_bytes()
    return {"status": "supplied", "sha256": hashlib.sha256(raw).hexdigest(), "path": path.name}


def _wheel_metadata(path: Path) -> dict[str, str]:
    with zipfile.ZipFile(path) as archive:
        candidates = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        if len(candidates) != 1:
            raise ValueError(f"wheel must contain exactly one METADATA file: {path}")
        fields: dict[str, str] = {}
        for line in archive.read(candidates[0]).decode("utf-8").splitlines():
            key, separator, value = line.partition(": ")
            if separator and key in {"Name", "Version", "Requires-Python"}:
                fields[key] = value
        return fields
