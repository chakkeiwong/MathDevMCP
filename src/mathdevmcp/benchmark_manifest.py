from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import contract_metadata


@dataclass(frozen=True)
class BenchmarkManifestEntry:
    name: str
    purpose: str
    privacy: str
    in_git: bool
    status: str


def benchmark_manifest() -> dict:
    entries = [
        BenchmarkManifestEntry("parser_provenance", "Validate labels, environments, and source spans.", "synthetic_or_sanitized", True, "active"),
        BenchmarkManifestEntry("proof_false_confidence", "Ensure false claims and unsupported notation do not verify.", "synthetic", True, "active"),
        BenchmarkManifestEntry("code_doc_consistency", "Seed missing operations and equation/code mismatches.", "synthetic_or_sanitized", True, "active"),
        BenchmarkManifestEntry("assumption_detection", "Measure missing assumption detection.", "synthetic_or_sanitized", True, "planned"),
        BenchmarkManifestEntry("private_department_corpus", "Evaluate real finance/econ documents and code.", "private", False, "external_required"),
    ]
    return {"ok": True, "entries": [asdict(entry) for entry in entries], "metadata": contract_metadata("benchmark_manifest")}
