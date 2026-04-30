"""Verify that docs/clients/workflow-rules.md embeds the same rules text
that ships in the package as `mathdevmcp._workflow_rules.WORKFLOW_RULES`.

The package data is the single source of truth (CLI `install-rules`
reads from there). The doc copy exists for human reading; this test
catches drift between the two.
"""

from __future__ import annotations

import re
from pathlib import Path

from mathdevmcp._workflow_rules import WORKFLOW_RULES


ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "clients" / "workflow-rules.md"


_FENCE = re.compile(r"```text\n(.*?)\n```", re.DOTALL)


def _extracted_rules_block() -> str:
    text = DOC.read_text(encoding="utf-8")
    match = _FENCE.search(text)
    assert match is not None, f"{DOC} does not contain a ```text fenced block"
    return match.group(1).rstrip("\n") + "\n"


def test_doc_rules_block_matches_package_constant():
    extracted = _extracted_rules_block()
    assert extracted == WORKFLOW_RULES, (
        f"docs/clients/workflow-rules.md is out of sync with "
        f"mathdevmcp._workflow_rules.WORKFLOW_RULES. Update the doc by "
        f"running:\n\n"
        f"  PYTHONPATH=src python -c "
        f"'from mathdevmcp._workflow_rules import WORKFLOW_RULES; print(WORKFLOW_RULES, end=\"\")' "
        f"\\\n    | (echo '<...preserve doc preamble through the ```text fence...>'; cat) "
        f"# or just paste the block manually"
    )
