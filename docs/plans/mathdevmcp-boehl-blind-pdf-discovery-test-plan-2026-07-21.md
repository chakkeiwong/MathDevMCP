# MathDevMCP Boehl Blind PDF Discovery Test Plan

Date: 2026-07-21

Status: approved for execution after skeptical audit

## Research Intent Ledger

| Field | Definition |
| --- | --- |
| Main question | Given only the Boehl main-paper and appendix PDFs, what mathematical, reconstruction, consistency, and source-interface defects can a fresh Codex agent discover while using the public MathDevMCP workflow? |
| Candidate under test | The current experimental ResearchAssistant PDF intake plus the current public MathDevMCP functions, used by a fresh-context Codex agent. |
| Expected failure mode | PDF extraction loses mathematical structure; generic tools inspect equations in isolation; the agent supplies most semantic reasoning; important findings disappear from the final report. |
| Promotion criterion | Descriptive issue-level recall against the independently frozen committee inventory, with provenance showing which findings originated in MathDevMCP output and which required agent inference. This single case cannot promote general PDF readiness. |
| Promotion veto | Any answer-key leakage before the discovery artifact is frozen; report-derived labels, locations, issue count, or issue classes in the discovery prompt; inability to identify the exact commands and evidence behind findings. |
| Continuation veto | Source PDFs unavailable or changed; fresh agent reads a forbidden answer-key artifact; output is not frozen before comparison. |
| Repair trigger | Low recall, unusable payload, missing source anchors, unreliable extraction, or findings produced only through unrestricted agent reasoning. |
| Explanatory diagnostics | Runtime, parser availability, output size, abstentions, false positives, and direct rendered-page inspections. |
| Must not be concluded | General PDF capability, paper validity, exact solution or estimation validity, or that a fresh-agent finding was produced by MathDevMCP itself unless the raw tool output contains it. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the current system discover, rather than merely confirm, defects in these two PDFs? |
| Exact baseline | A fresh-context Codex agent receives the two PDF paths, repository instructions, and access to public MathDevMCP functions. It receives no committee report, prior Boehl audit, report-derived labels, known issue count, or expected issue taxonomy. |
| Primary measure | Descriptive exact/partial/missed matching of the frozen blind findings to the committee's independently frozen seven-item paper/appendix inventory. |
| Veto diagnostics | Any forbidden-artifact access or prompt leakage invalidates blind recall. Source hash drift invalidates source comparability. |
| Explanatory-only measures | Newly discovered issues, payload size, parser count, runtime, and qualitative usefulness. These do not compensate for missed answer-key issues. |
| Non-claims | This one-document-pair test does not estimate population precision/recall, certify either PDF, or isolate model ability from orchestration quality. |
| Preserved artifact | `docs/reviews/boehl-qe-blind-discovery-2026-07-21/` containing the immutable discovery report, command manifest, comparison matrix, and final result. |

## Discovery Isolation

The discovery agent must use a fresh conversation context. It may inspect the
two source PDFs, current MathDevMCP code and public documentation needed to run
the tools, and ResearchAssistant only through the current MathDevMCP provider
route. It must not inspect, search, list, or infer content from:

- `docs/reviews/boehl-qe-pdf-audit-2026-07-21/`;
- `docs/plans/mathdevmcp-researchassistant-pdf-integration-and-boehl-audit-plan-2026-07-21.md`;
- `docs/plans/mathdevmcp-researchassistant-pdf-integration-and-boehl-audit-result-2026-07-21.md`;
- `/home/chakwong/python/DynareMCP/docs/AIpostdoc/finalBGS/bgs_final_committee_report_d447.tex`;
- any file whose purpose is to summarize, review, index, or answer the Boehl
  paper's known defects.

The prompt must not disclose how many defects are expected, their labels,
locations, categories, or conclusions.

## Discovery Output Contract

The fresh agent must write only these two discovery-stage artifacts:

1. `blind-discovery.md`: findings with source page/equation anchors, exact
   defect or concern, mathematical reasoning, confidence, unresolved evidence,
   and direct classification.
2. `blind-run-manifest.md`: commands and public functions used, source hashes,
   environment facts, parser status, runtime when available, and forbidden-path
   compliance declaration.

Every finding must carry one provenance class:

- `raw_mathdevmcp_finding`: explicitly present in a public MathDevMCP result;
- `agent_inference_from_mathdevmcp_evidence`: reasoned by the fresh agent from
  content or localization returned by MathDevMCP;
- `direct_pdf_inspection`: found through independent page/text inspection after
  MathDevMCP use;
- `not_checked`.

The discovery report must be complete before the answer key is opened. After
the agent finishes, the supervisor records SHA-256 digests for both artifacts.
No discovery-stage file may then be edited. Evaluation goes in separate files.

## Evaluation Protocol

1. Verify forbidden paths were not named in the discovery manifest or command
   list and inspect the agent transcript available to the supervisor.
2. Hash and freeze the discovery artifacts.
3. Open the committee report and the already source-checked issue inventory.
4. Match each committee issue to the frozen discovery report as `exact`,
   `partial`, or `missed`; quote the blind finding identifier and preserve its
   provenance class.
5. Classify unmatched blind findings as source-supported additions,
   unresolved questions, duplicates, or false positives.
6. Report separately:
   - raw MathDevMCP discovery recall;
   - fresh-agent plus MathDevMCP discovery recall;
   - direct-inspection additions;
   - false positives and abstentions.

Because there is one paper/appendix pair and no sampling design, all recall
figures are descriptive. No statistical ranking or general capability claim is
supported.

## Skeptical Plan Audit

| Risk checked | Verdict and repair |
| --- | --- |
| Wrong baseline | Repaired. The earlier guided seven-label run is not the baseline. This run starts from two PDFs only. |
| Proxy promoted to criterion | Repaired. Issue count, diagnostic volume, and parser success are explanatory only; answer-key issue matching is primary. |
| Missing stop conditions | Passed. Leakage, source drift, or absent immutable output stops the test. |
| Unfair comparison | Passed with limitation. The report is an answer key, not prompt context. Exact, partial, and missed categories permit narrower or differently worded discoveries. |
| Hidden assumptions | Recorded. This tests a fresh Codex agent using MathDevMCP, not an autonomous deterministic MathDevMCP pipeline. Attribution classes prevent conflation. |
| Stale context | Repaired. `fork_turns=none` and explicit forbidden paths prevent inheritance of the current conversation and prior audit. |
| Environment mismatch | Recorded. The current worktree contains the experimental PDF bridge; the exact git state and source hashes must appear in the manifest. |
| Artifacts answer the question | Passed. Findings are frozen before comparison and raw-tool versus agent-derived provenance is mandatory. |

The plan survives skeptical audit. The largest residual limitation is that a
fresh Codex agent may possess general pretrained knowledge of the published
paper, which cannot be measured locally. It receives no local answer key or
task-specific hints, and any resulting recall remains a case-study diagnostic.

## Stop And Handoff Conditions

Stop as invalid if an answer-key artifact is accessed before discovery freeze,
or if the source hashes differ from the comparator audit. Otherwise continue
through evaluation even when discovery recall is zero. A low-recall candidate
result is evidence about the current workflow and triggers repair; it is not an
invalid experiment.

Close only when the discovery artifacts are hashed, the comparison matrix is
written, provenance-separated recall is reported, false positives are reviewed
against the PDFs, and limitations/non-claims are explicit.
