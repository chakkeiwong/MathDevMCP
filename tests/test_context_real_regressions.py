from __future__ import annotations

from pathlib import Path

from mathdevmcp.context_evidence import build_context_evidence_payload


ROOT = Path(__file__).resolve().parent.parent
CARD_DIGESTS = {
    "7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0",
    "d9f072ac09016b17d5630556329bc871e79386a442c8c26587ef39a0134eeaac",
}


def test_card_pi_resolves_policy_or_ambiguous_never_posterior() -> None:
    payload = build_context_evidence_payload(ROOT)
    entries = [
        item for item in payload["symbol_resolution_ledger"]["entries"]
        if item["obligation_digest"] in CARD_DIGESTS
    ]

    assert len(entries) == 2
    for entry in entries:
        pi = next(item for item in entry["resolutions"] if item["symbol"] == r"\pi")
        assert pi["state"] in {"resolved", "ambiguous"}
        assert pi["role"] in {"policy_candidate", None}
        assert pi["role"] != "posterior_candidate"


def test_frozen_entries_have_exact_one_file_context_closures() -> None:
    payload = build_context_evidence_payload(ROOT)
    frozen = payload["frozen_regressions"]["entries"]

    assert len(frozen) == 4
    assert payload["frozen_regressions"]["all_entries_single_reachable_file"] is True
    assert all(item["diagnostic_kinds"] == [] for item in frozen)
    assert {
        item["entry_source_digest"] for item in frozen
    } == {
        "dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8",
        "d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1",
    }
