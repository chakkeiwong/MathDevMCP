from __future__ import annotations

import argparse
from copy import deepcopy
import importlib.util
from pathlib import Path
import py_compile
import sys
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "scripts/run_p08_frozen_validation.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("p08_runner_for_tests", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


p08 = _load_runner()


def _capability_extraction() -> dict:
    source_ref = p08.SOURCE_BINDINGS["risky"]["ref"]
    source_digest = p08.SOURCE_BINDINGS["risky"]["sha256"]
    raw = (ROOT / source_ref).read_bytes()
    records = [
        {
            "label": "eq:risky-cash-flow",
            "obligation_digest": p08.P08B_SOURCE_PROJECTIONS[
                "eq:risky-cash-flow"
            ]["obligation_digest"],
            "owned_spans": [
                {"start_byte": 6844, "end_byte": 6958},
                {"start_byte": 6963, "end_byte": 7117},
            ],
            "source_math": raw[6844:7117].decode("utf-8"),
            "normalized_target": {
                "complete_lhs_rhs": True,
                "display_text": "e(k,k',b,b',z;\\widetilde r) = (1-\\tau)\\pi(k,z) -\\psi(k'-(1-\\delta)k,k) -\\bigl(k'-(1-\\delta)k\\bigr) +\\frac{b'}{1+\\widetilde r(z,k',b')} +\\frac{\\tau \\widetilde r(z,k',b')b'} {(1+\\widetilde r(z,k',b'))(1+r)} -b",
                "kind": "equality",
                "members": [
                    "e(k,k',b,b',z;\\widetilde r)",
                    "(1-\\tau)\\pi(k,z) -\\psi(k'-(1-\\delta)k,k) -\\bigl(k'-(1-\\delta)k\\bigr) +\\frac{b'}{1+\\widetilde r(z,k',b')} +\\frac{\\tau \\widetilde r(z,k',b')b'} {(1+\\widetilde r(z,k',b'))(1+r)} -b",
                ],
                "normalization_version": "p02_latex_surface_normalization@1",
            },
        },
        {
            "label": "eq:cashflow-rate-derivative",
            "obligation_digest": p08.P08B_SOURCE_PROJECTIONS[
                "eq:cashflow-rate-derivative"
            ]["obligation_digest"],
            "owned_spans": [{"start_byte": 28649, "end_byte": 28775}],
            "source_math": raw[28649:28775].decode("utf-8"),
            "normalized_target": {
                "complete_lhs_rhs": True,
                "display_text": "e_{\\widetilde r} = \\frac{b'}{(1+\\widetilde r)^2} \\left(-1+\\frac{\\tau}{1+r}\\right)",
                "kind": "equality",
                "members": [
                    "e_{\\widetilde r}",
                    "\\frac{b'}{(1+\\widetilde r)^2} \\left(-1+\\frac{\\tau}{1+r}\\right)",
                ],
                "normalization_version": "p02_latex_surface_normalization@1",
            },
        },
    ]
    selected = [
        {
            **record,
            "document": {
                "file": source_ref,
                "source_digest": source_digest,
            },
        }
        for record in records
    ]
    return {"groups": [{"result": {"obligations": selected}}]}


def _manifest_and_identity() -> tuple[dict, dict]:
    manifest = {
        "run_id": "run-1",
        "run_root": "p08/runs/run-1",
        "run_binding_digest": "1" * 64,
    }
    identity = {"code_identity_digest": "2" * 64, "files": []}
    return manifest, identity


def _ready_preflight_records() -> tuple[dict, dict, dict, dict, dict]:
    import mathdevmcp.sympy_derivative_adapter as adapter

    manifest, identity = _manifest_and_identity()
    expression, target = p08._capability_obligations(_capability_extraction())
    request = adapter.build_derivative_request(
        source_expression_obligation_digest=expression["obligation_digest"],
        source_target_obligation_digest=target["obligation_digest"],
    )
    formalization = p08._formalization_record(manifest, identity, expression, target, request)
    tool_ledger = p08._tool_ledger_record(
        manifest, identity, "READY_EXACT_REGISTERED_ROUTE", None
    )
    ladder = p08._capability_ladder_record(
        manifest, identity, "READY_EXACT_REGISTERED_ROUTE"
    )
    preflight = p08._bound_record(
        p08.CAPABILITY_SCHEMA,
        manifest,
        identity,
        {
            "status": "READY_EXACT_REGISTERED_ROUTE",
            "candidate_id": "eq:cashflow-rate-derivative",
            "candidate_obligation_digest": target["obligation_digest"],
            "formalization": {
                "source_expression": "g(rt) = bp/(1 + rt) + tau*rt*bp/((1 + rt)*(1 + r))",
                "source_target": "d g(rt)/d rt = bp/(1 + rt)^2 * (-1 + tau/(1 + r))",
                "differentiated_variable": "rt",
                "held_constant": ["bp", "tau", "r"],
                "domains": {"rt": "real", "bp": "real", "tau": "real", "r": "real"},
                "domain_assumptions": [
                    "1 + rt != 0",
                    "1 + r != 0",
                    "g is differentiable with respect to rt on the nonsingular real domain",
                ],
            },
            "adapter_descriptor": adapter.derivative_capability_descriptor(),
            "dry_request": request,
            "formalization_digest": formalization["formalization_digest"],
            "tool_ledger_digest": tool_ledger["tool_ledger_digest"],
            "ladder_digest": ladder["ladder_digest"],
            "selected_route": "SymPy deterministic derivative construction plus independent exact-zero difference check",
            "route_gap": None,
            "required_repair": None,
            "backend_request_count": 0,
            "readiness_guard": {
                "action": "p08b_capability_preflight",
                "forbidden_attempt_count": 0,
                "forbidden_attempts": [],
            },
            "publication_enabled": False,
            "non_claims": [
                "Preflight does not import or execute SymPy.",
                "A generated formalization is not proof or backend evidence.",
            ],
        },
    )
    preflight["preflight_digest"] = p08._digest(preflight)
    return preflight, formalization, tool_ledger, ladder, _capability_extraction()


def _write_candidate_bundle(tmp_path: Path, *, aggregate_overflow: bool = False):
    import mathdevmcp.sympy_derivative_adapter as adapter

    root = tmp_path
    run_root = root / "run"
    candidate_root = run_root / "p08b/backend/eq_cashflow_rate_derivative"
    candidate_root.mkdir(parents=True)
    manifest, identity = _manifest_and_identity()
    expression, target = p08._capability_obligations(_capability_extraction())
    request = adapter.build_derivative_request(
        source_expression_obligation_digest=expression["obligation_digest"],
        source_target_obligation_digest=target["obligation_digest"],
    )
    native = adapter.canonical_json_bytes(request)
    command = [
        p08.P08_PYTHON,
        *p08.P08_WORKER_PYTHON_FLAGS,
        str(run_root / "code-snapshot" / p08.DERIVATIVE_ADAPTER_REF),
    ]
    if aggregate_overflow:
        stdout = b""
        stderr = b"x" * p08.P08_RAW_STREAM_LIMIT
        execution = {
            "kind": "subprocess",
            "runner_id": p08.DERIVATIVE_ADAPTER_VERSION,
            "command": command,
            "executable": p08.P08_PYTHON,
            "environment": dict(p08.P08_WORKER_ENVIRONMENT),
            "exit_code": 1,
            "timed_out": False,
            "overflow": False,
            "wall_time_ms": 10,
            "live_tool_executed": True,
            "run_id": manifest["run_id"],
            "run_binding_digest": manifest["run_binding_digest"],
            "code_identity_digest": identity["code_identity_digest"],
        }
        result = adapter.build_derivative_result(
            request=request,
            worker_record=None,
            native_input=native,
            stdout=stdout,
            stderr=stderr,
            execution=execution,
            failure_status="execution_error",
            failure_reason="r" * 780_000,
        )
    else:
        worker = adapter.compute_worker_record(request)
        stdout = adapter.worker_record_bytes(worker, request)
        stderr = b""
        execution = {
            "kind": "subprocess",
            "runner_id": p08.DERIVATIVE_ADAPTER_VERSION,
            "command": command,
            "executable": p08.P08_PYTHON,
            "environment": dict(p08.P08_WORKER_ENVIRONMENT),
            "exit_code": 0,
            "timed_out": False,
            "overflow": False,
            "wall_time_ms": 10,
            "live_tool_executed": True,
            "run_id": manifest["run_id"],
            "run_binding_digest": manifest["run_binding_digest"],
            "code_identity_digest": identity["code_identity_digest"],
        }
        result = adapter.build_derivative_result(
            request=request,
            worker_record=worker,
            native_input=native,
            stdout=stdout,
            stderr=stderr,
            execution=execution,
        )
    raw_files = {
        "native-input.json": native,
        "stdout.bin": stdout,
        "stderr.bin": stderr,
        "result.json": adapter.canonical_json_bytes(result),
    }
    for name, raw in raw_files.items():
        (candidate_root / name).write_bytes(raw)
    file_records = [
        {"name": name, "sha256": p08._digest(raw_files[name]), "byte_count": len(raw_files[name])}
        for name in ("native-input.json", "stdout.bin", "stderr.bin", "result.json")
    ]
    bundle_manifest = p08._bound_record(
        p08.CAPABILITY_MANIFEST_SCHEMA,
        manifest,
        identity,
        {
            "candidate_id": "eq:cashflow-rate-derivative",
            "request_digest": request["request_digest"],
            "files": file_records,
            "fixed_overhead_bytes": p08.P08_BUNDLE_OVERHEAD,
            "max_artifact_bytes": p08.P08_BUNDLE_LIMIT,
            "publication_enabled": False,
        },
    )
    (candidate_root / "manifest.json").write_bytes(p08._canonical(bundle_manifest))
    return root, run_root, candidate_root, manifest, identity, request


def _run_synthetic_verifier(monkeypatch: pytest.MonkeyPatch, bundle) -> dict:
    root, run_root, _candidate_root, manifest, identity, request = bundle
    monkeypatch.setattr(p08, "_workspace", lambda: root)
    monkeypatch.setattr(p08, "_open_run", lambda *args: (run_root, manifest, identity))
    monkeypatch.setattr(p08, "_require_p08a_pass", lambda *args: {})
    monkeypatch.setattr(p08, "_verify_preflight", lambda *args: {"dry_request": request})
    monkeypatch.setattr(p08, "_record_command", lambda *args: None)
    monkeypatch.setattr(p08, "_loaded_repo_modules", lambda *args: [])
    monkeypatch.setattr(p08, "_verify_code_identity", lambda *args: identity)
    return p08.command_verify_capability(argparse.Namespace(run_root="ignored"))


def test_plan_constants_bind_exact_frozen_inputs_and_group_order() -> None:
    assert p08.SOURCE_BINDINGS["card"]["sha256"] == (
        "dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8"
    )
    assert p08.SOURCE_BINDINGS["risky"]["sha256"] == (
        "d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1"
    )
    assert [item[0] for item in p08.EXTRACTION_GROUPS] == [
        "card_capability",
        "card_focus",
        "risky_capability",
        "risky_focus",
    ]
    assert p08.EXTRACTION_GROUPS[3][2] == ("prop:interior-foc",)


def test_context_requests_are_pre_registered_without_self_labels() -> None:
    assert set(p08.CONTEXT_SPECS) == {
        "eq:panel-cf-primitive",
        "eq:incremental-cash-flow",
        "eq:panel-npv-functional",
        "eq:incremental-npv",
        "eq:risky-cash-flow",
        "eq:cashflow-rate-derivative",
        "eq:cashflow-total-k",
        "eq:cashflow-total-b",
        "eq:foc-k",
        "eq:foc-b",
    }
    assert all(label not in subjects for label, (_, subjects) in p08.CONTEXT_SPECS.items())


def test_validate_obligation_reconstructs_exact_source_and_rejects_mutation() -> None:
    from mathdevmcp.document_derivation_tree import extract_document_derivation_obligations

    source = ROOT / p08.SOURCE_BINDINGS["risky"]["ref"]
    result = extract_document_derivation_obligations(
        source,
        focus_labels=["eq:cashflow-rate-derivative"],
    )
    obligation = result["obligations"][0]
    p08._validate_obligation_source(ROOT, obligation)

    mutated = deepcopy(obligation)
    mutated["source_math"] += " "
    with pytest.raises(p08.Phase08Error, match="reconstruction"):
        p08._validate_obligation_source(ROOT, mutated)


def test_card_capability_operators_exclude_npv_operators() -> None:
    extraction = p08._extract(ROOT)
    card = next(item for item in extraction["groups"] if item["group_id"] == "card_capability")
    inventories = [set(item["operator_inventory"]) for item in card["result"]["obligations"]]
    assert all("summation" not in item and "conditional_expectation" not in item for item in inventories)
    assert extraction["backend_request_count"] == 0
    assert extraction["publication_enabled"] is False


def test_risky_proposition_remains_context_container_with_two_children() -> None:
    extraction = p08._extract(ROOT)
    risky = next(item for item in extraction["groups"] if item["group_id"] == "risky_focus")
    assert risky["requested_labels"] == ["prop:interior-foc"]
    assert [item["label"] for item in risky["result"]["obligations"]] == ["eq:foc-k", "eq:foc-b"]
    assert [item["label"] for item in risky["result"]["targets"]] == ["eq:foc-k", "eq:foc-b"]
    assert all(item["parent_label"] == "prop:interior-foc" for item in risky["result"]["targets"])


def test_resolve_context_rejects_explicit_target_span(monkeypatch: pytest.MonkeyPatch) -> None:
    extraction = p08._extract(ROOT)
    import mathdevmcp.document_context_graph as context_graph

    original = context_graph.resolve_context_requirement

    def injected(graph, obligation, request):
        result = original(graph, obligation, request)
        if result["candidates"]:
            result["candidates"][0]["applicability_state"] = "explicit"
            result["candidates"][0]["target_span_match"] = True
        return result

    monkeypatch.setattr(context_graph, "resolve_context_requirement", injected)
    with pytest.raises(p08.Phase08Error, match="target span"):
        p08._resolve_context(ROOT, extraction)


def test_self_label_only_context_never_source_supports(tmp_path: Path) -> None:
    from mathdevmcp.document_context_graph import build_context_dependency_graph, resolve_context_requirement

    raw = b"\\begin{equation}x=y\\label{eq:self}\\end{equation}\n"
    source = tmp_path / "entry.tex"
    source.write_bytes(raw)
    budget = {
        "max_files": 1,
        "max_bytes": 4096,
        "max_nodes": 64,
        "max_edges": 128,
        "max_dependency_expansions": 1,
    }
    graph = build_context_dependency_graph(
        tmp_path,
        "entry.tex",
        expected_entry_source_digest=p08._digest(raw),
        budget=budget,
    )
    obligation = {
        "obligation_digest": "1" * 64,
        "adapter_eligible": True,
        "extraction_state": "valid_complete",
        "label": "eq:self",
        "owned_spans": [{"start_byte": 0, "end_byte": len(raw)}],
        "document": {"file": "entry.tex"},
    }
    request = {
        "obligation_digest": "1" * 64,
        "entry_source_digest": p08._digest(raw),
        "requirement_id": "p08_self_evidence",
        "requirement_predicate": "An independent declaration for x and y is available.",
        "requirement_subjects": ["x", "y"],
        "required_node_kinds": ["definition", "assumption", "notation_declaration", "proposition"],
        "required_edge_kinds": ["input", "include", "contains", "references"],
        "required_files": ["entry.tex"],
        "budget": budget,
    }
    result = resolve_context_requirement(graph, obligation, request)
    assert result["terminal_state"] in {"candidate_assumption", "not_found_after_search"}


def test_open_run_rejects_parent_latest_and_cross_run_binding(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(p08, "PHASE_ROOT", Path("p08-root"))
    monkeypatch.setattr(p08, "_workspace", lambda: tmp_path)
    with pytest.raises(p08.Phase08Error, match="exact immutable"):
        p08._open_run(tmp_path, "p08-root/runs")
    with pytest.raises(p08.Phase08Error, match="latest"):
        p08._open_run(tmp_path, "p08-root/runs/latest")


def test_code_identity_rejects_live_byte_drift(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source_ref = "scripts/run_p08_frozen_validation.py"
    source = tmp_path / source_ref
    source.parent.mkdir(parents=True)
    source.write_bytes(b"original")
    snapshot = tmp_path / "run/code-snapshot" / source_ref
    snapshot.parent.mkdir(parents=True)
    snapshot.write_bytes(b"original")
    identity = {
        "schema_version": p08.CODE_SCHEMA,
        "run_id": "run",
        "run_binding_digest": "2" * 64,
        "head": "3" * 40,
        "dirty_paths": [],
        "required_refs": [source_ref],
        "files": [{"ref": source_ref, "sha256": p08._digest(b"original"), "byte_count": 8, "dirty": False}],
        "boundary": "test",
    }
    identity["code_identity_digest"] = p08._digest(identity)
    (tmp_path / "run/code-identity.json").write_bytes(p08._canonical(identity))
    monkeypatch.setattr(p08, "REQUIRED_CODE_REFS", frozenset({source_ref}))
    p08._verify_code_identity(tmp_path, tmp_path / "run")
    source.write_bytes(b"changed!")
    with pytest.raises(p08.Phase08Error, match="code drift"):
        p08._verify_code_identity(tmp_path, tmp_path / "run")


def test_open_run_rejects_manifest_code_identity_cross_binding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    phase = Path("p08-root")
    run_root = tmp_path / phase / "runs/run-1"
    run_root.mkdir(parents=True)
    run_ref = (phase / "runs/run-1").as_posix()
    binding = p08._digest({"run_id": "run-1", "run_root": run_ref, "phase": "P08"})
    manifest = {
        "schema_version": p08.RUN_SCHEMA,
        "run_id": "run-1",
        "run_root": run_ref,
        "run_binding_digest": binding,
        "code_identity_digest": "1" * 64,
        "python_executable": p08.P08_PYTHON,
    }
    (run_root / "run-manifest.json").write_bytes(p08._canonical(manifest))
    identity = {
        "run_id": "run-1",
        "run_binding_digest": binding,
        "code_identity_digest": "2" * 64,
    }
    monkeypatch.setattr(p08, "PHASE_ROOT", phase)
    monkeypatch.setattr(p08, "_verify_code_identity", lambda *args: identity)
    with pytest.raises(p08.Phase08Error, match="cross-binding"):
        p08._open_run(tmp_path, run_ref)


def test_capability_preflight_is_nonexecuting_and_requires_adapter_repair(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    manifest = {"run_id": "run", "run_root": "p08/runs/run", "run_binding_digest": "1" * 64}
    identity = {"code_identity_digest": "2" * 64, "files": []}
    extraction = _capability_extraction()
    monkeypatch.setattr(p08, "_workspace", lambda: tmp_path)
    monkeypatch.setattr(p08, "_open_run", lambda root, path: (tmp_path, manifest, identity))
    monkeypatch.setattr(p08, "_require_p08a_pass", lambda *args: {})
    monkeypatch.setattr(p08, "_load_canonical", lambda path: extraction)
    monkeypatch.setattr(p08, "_verify_code_identity", lambda *args: identity)
    monkeypatch.setattr(p08, "_write_json_new", lambda *args: {})
    monkeypatch.setattr(p08, "_loaded_repo_modules", lambda *args: [])
    monkeypatch.setattr(p08, "_record_command", lambda *args: None)
    result = p08.command_capability_preflight(argparse.Namespace(run_root="ignored"))
    assert result["status"] == "BLOCKED_ADAPTER_REPAIR_REQUIRED"
    assert result["backend_request_count"] == 0


@pytest.mark.parametrize("mutation", ["source_math", "normalized_target", "document"])
def test_capability_obligations_reject_source_projection_drift(mutation: str) -> None:
    extraction = _capability_extraction()
    obligation = extraction["groups"][0]["result"]["obligations"][0]
    if mutation == "source_math":
        obligation["source_math"] += " "
    elif mutation == "normalized_target":
        obligation["normalized_target"]["display_text"] += " "
    else:
        obligation["document"]["source_digest"] = "0" * 64
    with pytest.raises(p08.Phase08Error, match="source-to-scalar projection"):
        p08._capability_obligations(extraction)


def test_capability_obligations_reject_duplicate_label_even_with_same_digest() -> None:
    extraction = _capability_extraction()
    obligations = extraction["groups"][0]["result"]["obligations"]
    obligations.append(deepcopy(obligations[0]))
    with pytest.raises(p08.Phase08Error, match="absent or inconsistent"):
        p08._capability_obligations(extraction)


@pytest.mark.parametrize(
    "mutation",
    [
        "adapter_version",
        "operation",
        "request_schema",
        "worker_schema",
        "result_schema",
        "missing_api",
        "descriptor",
        "request",
    ],
)
def test_adapter_readiness_rejects_every_registered_handshake_mutation(
    mutation: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    import mathdevmcp.sympy_derivative_adapter as adapter

    fake = SimpleNamespace(
        SYMPY_DERIVATIVE_ADAPTER_VERSION=adapter.SYMPY_DERIVATIVE_ADAPTER_VERSION,
        SYMPY_DERIVATIVE_OPERATION=adapter.SYMPY_DERIVATIVE_OPERATION,
        SYMPY_DERIVATIVE_REQUEST_SCHEMA=adapter.SYMPY_DERIVATIVE_REQUEST_SCHEMA,
        SYMPY_DERIVATIVE_WORKER_SCHEMA=adapter.SYMPY_DERIVATIVE_WORKER_SCHEMA,
        SYMPY_DERIVATIVE_RESULT_SCHEMA=adapter.SYMPY_DERIVATIVE_RESULT_SCHEMA,
        derivative_capability_descriptor=adapter.derivative_capability_descriptor,
        build_derivative_request=adapter.build_derivative_request,
        validate_derivative_request=adapter.validate_derivative_request,
        canonical_json_bytes=adapter.canonical_json_bytes,
    )
    attribute_by_mutation = {
        "adapter_version": "SYMPY_DERIVATIVE_ADAPTER_VERSION",
        "operation": "SYMPY_DERIVATIVE_OPERATION",
        "request_schema": "SYMPY_DERIVATIVE_REQUEST_SCHEMA",
        "worker_schema": "SYMPY_DERIVATIVE_WORKER_SCHEMA",
        "result_schema": "SYMPY_DERIVATIVE_RESULT_SCHEMA",
    }
    if mutation in attribute_by_mutation:
        setattr(fake, attribute_by_mutation[mutation], "mutated")
    elif mutation == "missing_api":
        fake.validate_derivative_request = None
    elif mutation == "descriptor":
        fake.derivative_capability_descriptor = lambda: {"operation": "mutated"}
    else:
        fake.build_derivative_request = lambda **kwargs: {"candidate_id": "mutated"}
    monkeypatch.setattr(p08.importlib, "import_module", lambda name: fake)
    monkeypatch.delitem(sys.modules, "sympy", raising=False)
    expression, target = p08._capability_obligations(_capability_extraction())
    status, descriptor, request, error = p08._adapter_readiness(
        expression,
        target,
        {"files": [{"ref": p08.DERIVATIVE_ADAPTER_REF}]},
    )
    assert status == "BLOCKED_ADAPTER_REPAIR_REQUIRED"
    assert descriptor is None and request is None and error


def test_adapter_readiness_accepts_exact_pure_registered_handshake(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import mathdevmcp.sympy_derivative_adapter as adapter

    monkeypatch.setattr(p08.importlib, "import_module", lambda name: adapter)
    monkeypatch.delitem(sys.modules, "sympy", raising=False)
    expression, target = p08._capability_obligations(_capability_extraction())
    status, descriptor, request, error = p08._adapter_readiness(
        expression,
        target,
        {"files": [{"ref": p08.DERIVATIVE_ADAPTER_REF}]},
    )
    assert status == "READY_EXACT_REGISTERED_ROUTE"
    assert descriptor == adapter.derivative_capability_descriptor()
    assert request["candidate_id"] == "eq:cashflow-rate-derivative"
    assert error is None and "sympy" not in sys.modules


@pytest.mark.parametrize(
    ("artifact_name", "digest_key", "message"),
    [
        ("formalization.json", "formalization_digest", "formalization"),
        ("external-tool-ledger.json", "tool_ledger_digest", "external-tool ledger"),
        ("capability-ladder.json", "ladder_digest", "capability ladder"),
    ],
)
def test_preflight_reconstructs_formalization_tool_ledger_and_ladder(
    tmp_path: Path,
    artifact_name: str,
    digest_key: str,
    message: str,
) -> None:
    preflight, formalization, tool_ledger, ladder, extraction = _ready_preflight_records()
    manifest, identity = _manifest_and_identity()
    p08b = tmp_path / "p08b"
    p08a = tmp_path / "p08a"
    p08b.mkdir()
    p08a.mkdir()
    records = {
        "capability-preflight.json": preflight,
        "formalization.json": formalization,
        "external-tool-ledger.json": tool_ledger,
        "capability-ladder.json": ladder,
    }
    for name, record in records.items():
        (p08b / name).write_bytes(p08._canonical(record))
    (p08a / "extraction.json").write_bytes(p08._canonical(extraction))
    assert p08._verify_preflight(tmp_path, manifest, identity) == preflight

    mutated = deepcopy(records[artifact_name])
    mutated["publication_enabled"] = True
    mutated[digest_key] = p08._digest(
        {key: value for key, value in mutated.items() if key != digest_key}
    )
    (p08b / artifact_name).write_bytes(p08._canonical(mutated))
    with pytest.raises(p08.Phase08Error, match=message):
        p08._verify_preflight(tmp_path, manifest, identity)


def test_capability_ladder_and_run_reject_target_shopping(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest, identity = _manifest_and_identity()
    ladder = p08._capability_ladder_record(
        manifest, identity, "READY_EXACT_REGISTERED_ROUTE"
    )
    assert ladder["current_candidate_id"] == "eq:cashflow-rate-derivative"
    assert ladder["target_shopping_allowed"] is False
    assert [item["state"] for item in ladder["candidates"]] == [
        "ready",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
    ]
    monkeypatch.setattr(p08, "_workspace", lambda: tmp_path)
    monkeypatch.setattr(p08, "_open_run", lambda *args: (tmp_path, manifest, identity))
    monkeypatch.setattr(p08, "_require_p08a_pass", lambda *args: {})
    monkeypatch.setattr(p08, "_verify_preflight", lambda *args: {})
    args = argparse.Namespace(
        run_root="ignored",
        candidate="eq:cashflow-total-k",
        timeout_seconds=10,
        max_output_bytes=p08.P08_RAW_STREAM_LIMIT,
        max_artifact_bytes=p08.P08_BUNDLE_LIMIT,
    )
    with pytest.raises(p08.Phase08Error, match="fixed capability ladder"):
        p08.command_capability_run(args)


def test_capability_run_rejects_resource_limit_mutation_before_execution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest, identity = _manifest_and_identity()
    monkeypatch.setattr(p08, "_workspace", lambda: tmp_path)
    monkeypatch.setattr(p08, "_open_run", lambda *args: (tmp_path, manifest, identity))
    monkeypatch.setattr(p08, "_require_p08a_pass", lambda *args: {})
    monkeypatch.setattr(p08, "_verify_preflight", lambda *args: {})
    args = argparse.Namespace(
        run_root="ignored",
        candidate="eq:cashflow-rate-derivative",
        timeout_seconds=9,
        max_output_bytes=p08.P08_RAW_STREAM_LIMIT,
        max_artifact_bytes=p08.P08_BUNDLE_LIMIT,
    )
    with pytest.raises(p08.Phase08Error, match="reviewed exact values"):
        p08.command_capability_run(args)


@pytest.mark.parametrize("stream", ["stdout", "stderr"])
def test_bounded_worker_caps_each_output_stream(stream: str) -> None:
    target = "stdout" if stream == "stdout" else "stderr"
    command = [
        p08.P08_PYTHON,
        "-c",
        f"import sys; sys.{target}.buffer.write(b'x' * 4096); sys.{target}.buffer.flush()",
    ]
    result = p08._bounded_worker(
        command,
        b"",
        timeout_seconds=2,
        max_stdout_bytes=32,
        max_stderr_bytes=32,
    )
    assert result["overflow"] is True
    assert len(result[stream]) == 33
    assert len(result["stderr" if stream == "stdout" else "stdout"]) == 0


def test_bounded_worker_times_out_and_reaps_child() -> None:
    result = p08._bounded_worker(
        [p08.P08_PYTHON, "-c", "import time; time.sleep(5)"],
        b"",
        timeout_seconds=1,
        max_stdout_bytes=32,
        max_stderr_bytes=32,
    )
    assert result["timed_out"] is True
    assert result["exit_code"] is not None


def test_bounded_worker_closed_descriptors_still_obey_original_deadline() -> None:
    result = p08._bounded_worker(
        [
            p08.P08_PYTHON,
            "-c",
            "import os,time; os.close(0); os.close(1); os.close(2); time.sleep(5)",
        ],
        b"",
        timeout_seconds=1,
        max_stdout_bytes=32,
        max_stderr_bytes=32,
    )
    assert result["timed_out"] is True
    assert result["overflow"] is False
    assert result["exit_code"] is not None
    assert result["wall_time_ms"] < 2_000


def test_bounded_worker_rejects_oversized_native_input_without_launch() -> None:
    with pytest.raises(p08.Phase08Error, match="native input"):
        p08._bounded_worker(
            [p08.P08_PYTHON, "-c", "raise SystemExit(99)"],
            b"x" * (p08.P08_RAW_STREAM_LIMIT + 1),
            timeout_seconds=1,
            max_stdout_bytes=32,
            max_stderr_bytes=32,
        )


def test_bounded_worker_handles_simultaneous_input_and_output() -> None:
    native = b"x" * 100_000
    result = p08._bounded_worker(
        [
            p08.P08_PYTHON,
            "-c",
            "import sys; data=sys.stdin.buffer.read(); sys.stdout.buffer.write(data)",
        ],
        native,
        timeout_seconds=2,
        max_stdout_bytes=len(native),
        max_stderr_bytes=32,
    )
    assert result["exit_code"] == 0
    assert result["timed_out"] is False and result["overflow"] is False
    assert result["stdout"] == native and result["stderr"] == b""


def test_isolated_worker_ignores_shadow_sympy_and_sitecustomize(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import mathdevmcp.sympy_derivative_adapter as adapter

    hostile = tmp_path / "hostile"
    hostile.mkdir()
    marker = tmp_path / "hostile-imported"
    (hostile / "sympy.py").write_text(
        f"from pathlib import Path\nPath({str(marker)!r}).write_text('sympy')\n__version__='1.14.0'\n",
        encoding="utf-8",
    )
    (hostile / "sitecustomize.py").write_text(
        f"from pathlib import Path\nPath({str(marker)!r}).write_text('sitecustomize')\n",
        encoding="utf-8",
    )
    worker = tmp_path / "worker.py"
    worker.write_bytes((ROOT / p08.DERIVATIVE_ADAPTER_REF).read_bytes())
    request = adapter.build_derivative_request(
        source_expression_obligation_digest=p08.P08B_SOURCE_PROJECTIONS[
            "eq:risky-cash-flow"
        ]["obligation_digest"],
        source_target_obligation_digest=p08.P08B_SOURCE_PROJECTIONS[
            "eq:cashflow-rate-derivative"
        ]["obligation_digest"],
    )
    monkeypatch.setenv("PYTHONPATH", str(hostile))
    result = p08._bounded_worker(
        [p08.P08_PYTHON, *p08.P08_WORKER_PYTHON_FLAGS, str(worker)],
        adapter.canonical_json_bytes(request),
        timeout_seconds=10,
        max_stdout_bytes=p08.P08_RAW_STREAM_LIMIT,
        max_stderr_bytes=p08.P08_RAW_STREAM_LIMIT,
    )
    assert result["exit_code"] == 0
    assert result["timed_out"] is False and result["overflow"] is False
    record = adapter.parse_worker_stdout(result["stdout"], request)
    assert record["sympy_site_packages"] == adapter.SYMPY_SITE_PACKAGES
    assert record["sympy_origin"] == adapter.SYMPY_EXPECTED_ORIGIN
    assert record["sympy_origin_sha256"] == adapter.SYMPY_EXPECTED_ORIGIN_SHA256
    assert record["sympy_package_file_count"] == adapter.SYMPY_EXPECTED_PACKAGE_FILE_COUNT
    assert record["sympy_package_byte_count"] == adapter.SYMPY_EXPECTED_PACKAGE_BYTE_COUNT
    assert record["sympy_package_sha256"] == adapter.SYMPY_EXPECTED_PACKAGE_SHA256
    assert record["mpmath_version"] == adapter.MPMATH_EXPECTED_VERSION
    assert record["mpmath_origin"] == adapter.MPMATH_EXPECTED_ORIGIN
    assert record["mpmath_origin_sha256"] == adapter.MPMATH_EXPECTED_ORIGIN_SHA256
    assert record["mpmath_package_file_count"] == adapter.MPMATH_EXPECTED_PACKAGE_FILE_COUNT
    assert record["mpmath_package_byte_count"] == adapter.MPMATH_EXPECTED_PACKAGE_BYTE_COUNT
    assert record["mpmath_package_sha256"] == adapter.MPMATH_EXPECTED_PACKAGE_SHA256
    assert record["site_packages_module_roots"] == ["mpmath", "sympy"]
    assert not marker.exists()


def test_source_only_flags_bypass_valid_poisoned_adjacent_bytecode(tmp_path: Path) -> None:
    source = tmp_path / "probe.py"
    source.write_text("VALUE = 'poison'\n", encoding="utf-8")
    py_compile.compile(
        str(source),
        doraise=True,
        invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH,
    )
    source.write_text("VALUE = 'source'\n", encoding="utf-8")
    script = (
        f"import sys; sys.path.insert(0, {str(tmp_path)!r}); "
        "import probe; print(probe.VALUE)"
    )
    bytecode_read = p08._bounded_worker(
        [p08.P08_PYTHON, "-I", "-S", "-B", "-c", script],
        b"",
        timeout_seconds=5,
        max_stdout_bytes=32,
        max_stderr_bytes=256,
    )
    source_only = p08._bounded_worker(
        [p08.P08_PYTHON, *p08.P08_WORKER_PYTHON_FLAGS, "-c", script],
        b"",
        timeout_seconds=5,
        max_stdout_bytes=32,
        max_stderr_bytes=256,
    )
    assert bytecode_read["exit_code"] == 0 and bytecode_read["stdout"] == b"poison\n"
    assert source_only["exit_code"] == 0 and source_only["stdout"] == b"source\n"


@pytest.mark.parametrize(
    "flags",
    [
        ["-I", "-S", "-B"],
        ["-I", "-S", "-B", "-X", "pycache_prefix=/tmp/p08-unreviewed-cache"],
    ],
)
def test_worker_refuses_missing_or_mutated_cache_policy(
    tmp_path: Path, flags: list[str]
) -> None:
    import mathdevmcp.sympy_derivative_adapter as adapter

    worker = tmp_path / "worker.py"
    worker.write_bytes((ROOT / p08.DERIVATIVE_ADAPTER_REF).read_bytes())
    request = adapter.build_derivative_request(
        source_expression_obligation_digest="1" * 64,
        source_target_obligation_digest="2" * 64,
    )
    result = p08._bounded_worker(
        [p08.P08_PYTHON, *flags, str(worker)],
        adapter.canonical_json_bytes(request),
        timeout_seconds=5,
        max_stdout_bytes=256,
        max_stderr_bytes=1_024,
    )
    assert result["exit_code"] == 2
    assert result["stdout"] == b""
    assert b"worker runtime is not isolated and source-only" in result["stderr"]


@pytest.mark.parametrize("extra_kind", ["file", "directory"])
def test_candidate_directory_requires_exactly_five_regular_files(
    tmp_path: Path, extra_kind: str
) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    expected = {"native-input.json", "stdout.bin", "stderr.bin", "result.json", "manifest.json"}
    for name in expected:
        (candidate / name).write_bytes(b"")
    p08._require_exact_candidate_entries(candidate, expected)
    extra = candidate / "extra"
    if extra_kind == "file":
        extra.write_bytes(b"")
        message = "file set"
    else:
        extra.mkdir()
        message = "non-regular"
    with pytest.raises(p08.Phase08Error, match=message):
        p08._require_exact_candidate_entries(candidate, expected)


def test_candidate_aggregate_enforces_named_overhead_and_exact_limit() -> None:
    exact_sum, aggregate = p08._candidate_aggregate(
        [100, 200, 300, 400],
        500,
        p08.P08_BUNDLE_OVERHEAD,
        p08.P08_BUNDLE_LIMIT,
    )
    assert exact_sum == 1_500
    assert aggregate == 1_500 + p08.P08_BUNDLE_OVERHEAD
    with pytest.raises(p08.Phase08Error, match="aggregate limit"):
        p08._candidate_aggregate(
            [p08.P08_BUNDLE_LIMIT - p08.P08_BUNDLE_OVERHEAD],
            1,
            p08.P08_BUNDLE_OVERHEAD,
            p08.P08_BUNDLE_LIMIT,
        )


def test_capability_verifier_accepts_reconstructed_five_file_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    result = _run_synthetic_verifier(monkeypatch, _write_candidate_bundle(tmp_path))
    assert result["status"] == "backend_checked"
    assert result["can_promote"] is False
    assert result["formal_proof_certified"] is False


@pytest.mark.parametrize(
    "name",
    ["native-input.json", "stdout.bin", "stderr.bin", "result.json", "manifest.json"],
)
def test_capability_verifier_rejects_each_bundle_file_mutation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    bundle = _write_candidate_bundle(tmp_path)
    path = bundle[2] / name
    path.write_bytes(path.read_bytes() + b"x")
    with pytest.raises(p08.Phase08Error):
        _run_synthetic_verifier(monkeypatch, bundle)


def test_capability_verifier_enforces_aggregate_after_file_reconstruction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    bundle = _write_candidate_bundle(tmp_path)
    candidate_root = bundle[2]
    manifest_path = candidate_root / "manifest.json"
    manifest = p08._decode_canonical(manifest_path.read_bytes(), manifest_path)
    predecessor_sum = sum(item["byte_count"] for item in manifest["files"])
    synthetic_limit = predecessor_sum + len(manifest_path.read_bytes()) + p08.P08_BUNDLE_OVERHEAD - 1
    manifest["max_artifact_bytes"] = synthetic_limit
    manifest_path.write_bytes(p08._canonical(manifest))
    synthetic_limit = predecessor_sum + len(manifest_path.read_bytes()) + p08.P08_BUNDLE_OVERHEAD - 1
    manifest["max_artifact_bytes"] = synthetic_limit
    manifest_path.write_bytes(p08._canonical(manifest))
    monkeypatch.setattr(p08, "P08_BUNDLE_LIMIT", synthetic_limit)
    with pytest.raises(p08.Phase08Error, match="aggregate limit"):
        _run_synthetic_verifier(monkeypatch, bundle)


def _rewrite_result_and_manifest(candidate_root: Path, result: dict) -> None:
    import mathdevmcp.sympy_derivative_adapter as adapter

    result["result_digest"] = p08._digest(
        {key: value for key, value in result.items() if key != "result_digest"}
    )
    result_raw = adapter.canonical_json_bytes(result)
    (candidate_root / "result.json").write_bytes(result_raw)
    manifest_path = candidate_root / "manifest.json"
    manifest = p08._decode_canonical(manifest_path.read_bytes(), manifest_path)
    for record in manifest["files"]:
        if record["name"] == "result.json":
            record["sha256"] = p08._digest(result_raw)
            record["byte_count"] = len(result_raw)
    manifest_path.write_bytes(p08._canonical(manifest))


def test_capability_verifier_rejects_coordinated_worker_result_manifest_rewrite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import mathdevmcp.sympy_derivative_adapter as adapter

    bundle = _write_candidate_bundle(tmp_path)
    candidate_root = bundle[2]
    stdout_path = candidate_root / "stdout.bin"
    worker = p08._decode_canonical(stdout_path.read_bytes()[:-1], stdout_path)
    worker["difference"] = "0 + 0"
    forged_stdout = adapter.canonical_json_bytes(worker) + b"\n"
    stdout_path.write_bytes(forged_stdout)

    result_path = candidate_root / "result.json"
    result = p08._decode_canonical(result_path.read_bytes(), result_path)
    result["worker_record"] = worker
    result["raw_bindings"]["stdout.bin"] = {
        "sha256": p08._digest(forged_stdout),
        "byte_count": len(forged_stdout),
    }
    _rewrite_result_and_manifest(candidate_root, result)
    manifest_path = candidate_root / "manifest.json"
    manifest = p08._decode_canonical(manifest_path.read_bytes(), manifest_path)
    for record in manifest["files"]:
        if record["name"] == "stdout.bin":
            record["sha256"] = p08._digest(forged_stdout)
            record["byte_count"] = len(forged_stdout)
    manifest_path.write_bytes(p08._canonical(manifest))

    with pytest.raises(p08.Phase08Error, match="contract validation"):
        _run_synthetic_verifier(monkeypatch, bundle)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("can_promote", True, "contract validation"),
        ("publication_enabled", True, "contract validation"),
        ("formal_proof_certified", True, "contract validation"),
    ],
)
def test_capability_verifier_rejects_result_authority_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value,
    message: str,
) -> None:
    bundle = _write_candidate_bundle(tmp_path)
    result_path = bundle[2] / "result.json"
    result = p08._decode_canonical(result_path.read_bytes(), result_path)
    result[field] = value
    _rewrite_result_and_manifest(bundle[2], result)
    with pytest.raises(p08.Phase08Error, match=message):
        _run_synthetic_verifier(monkeypatch, bundle)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("run_id", "other-run"),
        ("run_binding_digest", "0" * 64),
        ("code_identity_digest", "0" * 64),
        ("executable", "/tmp/unregistered-python"),
        ("command", ["/tmp/unregistered-python", "worker.py"]),
        (
            "command",
            [p08.P08_PYTHON, "-I", "-S", "-B", "/tmp/worker.py"],
        ),
        (
            "command",
            [
                p08.P08_PYTHON,
                "-I",
                "-S",
                "-B",
                "-X",
                "pycache_prefix=/tmp/p08-unreviewed-cache",
                "/tmp/worker.py",
            ],
        ),
        ("environment", {"CUDA_VISIBLE_DEVICES": "-1", "PYTHONPATH": "src"}),
    ],
)
def test_capability_verifier_rejects_execution_envelope_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value,
) -> None:
    bundle = _write_candidate_bundle(tmp_path)
    result_path = bundle[2] / "result.json"
    result = p08._decode_canonical(result_path.read_bytes(), result_path)
    result["execution"][field] = value
    _rewrite_result_and_manifest(bundle[2], result)
    expected = (
        "contract validation"
        if field in {"environment", "command", "executable"}
        else "execution envelope"
    )
    with pytest.raises(p08.Phase08Error, match=expected):
        _run_synthetic_verifier(monkeypatch, bundle)
