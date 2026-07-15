## Findings

1. **High: the live run manifest contains false external-tool version provenance.** In `scripts/p02_governance.py:1114`, `_build_run_manifest_record()` reads `parser.get("versions", {})`, but the parser comparison exposes `version_receipts`. The resulting empty map causes LaTeXML and Pandoc to be recorded as `"not measured in blocked round"` at `scripts/p02_governance.py:1166` and `scripts/p02_governance.py:1173`. This contradicts the live evidence: both version receipts match, and all 28 invocations completed. Candidate reconstruction repeats the same faulty builder logic, so its self-consistency does not validate the false claim. Repair must derive version evidence from `version_receipts`, reopen the bound receipts and streams, and follow the append-only `REVISE` repair/close path.

2. **Medium: run-manifest validation cannot detect this provenance defect.** `src/mathdevmcp/extraction_evidence.py:3193` checks only that `external_tool_considerations` is a list. It does not validate exact fields or cross-bind availability/version claims to parser version receipts. Add strict validation and a focused mutation test proving that successful measured version receipts cannot yield the blocked-round fallback.

No other material defect was established. The 28 raw receipts close at exact `2+26`; call-class ceilings are `60/180` and `30/30`; timeout count is zero; source pre/post digests match; limitation-only states remain non-promotional; current is selected for all 13 cases; backend/source-edit ledgers are clean; and the 19-receipt chain and required hashes reconstruct.

Reviewed result round: `rr01`
Reviewed candidate SHA-256: `3cad00c92074e026d5c086b9c7e9539953edc39e7c2b5ce387397058c4a3b5f0`
Reviewed run manifest SHA-256: `73f0fee4bd51ffdb2487e7f12724908647879dfebcd1b0782f2e0d28020cc42f`
Reviewed result SHA-256: `37c691f89cae99eb19f7433c29df56583825b50ec5a02ee45e2f22a8cdf6297a`
Reviewed extraction bundle semantic digest: `2daf3c301940f2632a80592f7f603b89daa08db89944c5f3e768be4d0a7826db`
Reviewed extraction bundle-index SHA-256: `fd0c62608ed46e4412592b213fe52570a242a187583c52c178c1c2de674a3c68`
Reviewed parser comparison SHA-256: `6805640f8c65e06a6a7a9f3154959d9616fdb7a2ef498104ffc2c73511350341`
Reviewed mutation/ambiguity matrix SHA-256: `2c9b69212759257459221e7d330ba3ecf928bd7ad2ee7a68d59f85c1c90191e0`
Reviewed governance receipt-index SHA-256: `cac3a6325c56b0330037c70e5373f264ea35ad72117d521189cbf4da35cd7e33`
VERDICT: REVISE
