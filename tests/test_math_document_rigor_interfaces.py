import json
import subprocess
import sys
from pathlib import Path

from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import audit_math_document_rigor as server_audit_math_document_rigor
from mathdevmcp.mcp_server import plan_math_document_rigor_audit as server_plan_math_document_rigor_audit


ROOT = Path(__file__).resolve().parent.parent


def _write_fixture(path: Path) -> None:
    path.write_text(
        r"""
\section{Valuation}
\begin{equation}
\label{eq:toy-npv}
NPV = CF_0 + \beta CF_1
\end{equation}
""",
        encoding="utf-8",
    )


def test_mcp_facade_exposes_math_document_rigor(tmp_path: Path) -> None:
    tex = tmp_path / "toy.tex"
    output = tmp_path / "rigor.md"
    _write_fixture(tex)
    tools = {tool["name"]: tool for tool in list_mcp_tools()}

    plan = call_mcp_tool("plan_math_document_rigor_audit", {"tex_path": str(tex), "focus_labels": ["eq:toy-npv"]})
    result = call_mcp_tool(
        "audit_math_document_rigor",
        {
            "tex_path": str(tex),
            "focus_labels": ["eq:toy-npv"],
            "output_md": str(output),
            "max_labels": 1,
        },
    )

    assert tools["plan_math_document_rigor_audit"]["output_contract"] == "math_document_rigor_audit_plan"
    assert tools["audit_math_document_rigor"]["output_contract"] == "math_document_rigor_audit"
    assert plan["metadata"]["contract"] == "math_document_rigor_audit_plan"
    assert result["metadata"]["contract"] == "math_document_rigor_audit"
    assert result["coverage"]["target_file_only"] is True
    assert output.exists()


def test_fastmcp_server_wrappers_delegate_math_document_rigor(tmp_path: Path) -> None:
    tex = tmp_path / "toy.tex"
    _write_fixture(tex)

    plan = server_plan_math_document_rigor_audit(str(tex), focus_labels=["eq:toy-npv"], max_labels=1)
    result = server_audit_math_document_rigor(str(tex), focus_labels=["eq:toy-npv"], max_labels=1)

    assert plan["metadata"]["contract"] == "math_document_rigor_audit_plan"
    assert result["metadata"]["contract"] == "math_document_rigor_audit"


def test_cli_audit_math_document_rigor_writes_artifacts(tmp_path: Path) -> None:
    tex = tmp_path / "toy.tex"
    output_md = tmp_path / "rigor.md"
    output_json = tmp_path / "rigor.json"
    _write_fixture(tex)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "audit-math-document-rigor",
            str(tex),
            "--focus-label",
            "eq:toy-npv",
            "--output-md",
            str(output_md),
            "--output-json",
            str(output_json),
            "--max-labels",
            "1",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["metadata"]["contract"] == "math_document_rigor_audit"
    assert output_md.exists()
    assert output_json.exists()
