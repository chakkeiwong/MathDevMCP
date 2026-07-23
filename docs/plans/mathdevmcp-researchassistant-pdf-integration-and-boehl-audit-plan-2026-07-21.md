# MathDevMCP ResearchAssistant PDF Integration And Boehl Audit Plan

Date: 2026-07-21

Status: audited and ready for execution

## Objective

Add a bounded, typed MathDevMCP route for extracting local PDFs through the
ResearchAssistant checkout, then use that route and the existing LaTeX-native
MathDevMCP workflows to compare two Boehl quantitative-easing PDFs with the
mathematical issues recorded in the BGS committee report.

The engineering question is whether a provenance-bearing multi-parser intake
improves MathDevMCP's ability to locate and triage mathematical material in
PDF-only sources. The scientific question is which committee-report criticisms
are independently supported, absent, contradicted, or not decidable from the
paper, appendix, and available extraction evidence.

## Scope And Reader Contract

The target reader is a mathematically trained macroeconomist or maintainer who
must be able to decide:

1. whether the PDF extraction is adequate for a specific issue;
2. where the paper, appendix, and committee report agree or differ;
3. which MathDevMCP findings are actionable and which require manual source
   inspection; and
4. what the new cross-project function does and does not certify.

Canonical inputs are:

- `/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf`;
- `/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf`; and
- `/home/chakwong/python/DynareMCP/docs/AIpostdoc/finalBGS/bgs_final_committee_report_d447.tex`.

DynareMCP and ResearchAssistant are read-only. New implementation, tests, plan,
and review artifacts are written only in MathDevMCP. No paper or committee TeX
is edited. This is a document audit, not progress in DynareMCP's active
scholarly-readability mission and not authority for DSGE model construction,
calibration, simulation, estimation, publication, or claim promotion.

## Research Intent Ledger

| Field | Frozen value |
| --- | --- |
| Main question | Can ResearchAssistant-backed PDF intake support a reproducible MathDevMCP audit of the Boehl paper and appendix, and which BGS committee findings can that audit reproduce? |
| Mechanism under test | Reconciled multi-parser extraction bound to source bytes, parser identities, capability warnings, and the ResearchAssistant version, followed by bounded MathDevMCP and manual source comparison. |
| Expected failure mode | PDF formulas, symbols, page structure, footnotes, or citations are lost or corrupted; generic text diagnostics are mistaken for mathematical findings. |
| Promotion criterion | The adapter deterministically preserves source and provider identity, reports parser status/disagreement, fails closed on malformed output, keeps detailed content opt-in, and supports an inspectable comparison with issue-level source anchors. |
| Promotion veto | Wrong input digest; unparseable or schema-invalid provider output; omitted parser failures/capability limits; an issue classified as supported without an inspectable source anchor; or output presented as proof/certification. |
| Continuation veto | Neither PDF yields inspectable text; the canonical inputs change after hashing; the provider route cannot be invoked or emulated in focused tests; or the committee-report scope cannot be isolated. |
| Repair trigger | One parser fails while another succeeds; extracted math is ambiguous; payload is too large for MCP; stale hard-coded tool counts or documentation break the exposed surface. |
| Explanatory diagnostics | Parser agreement, text length, heading coverage, keyword hits, generic MathDevMCP diagnostic counts, and manual-review flags. |
| Forbidden conclusion | Parser agreement, a successful command, or a MathDevMCP finding does not prove the paper correct or incorrect, establish exact equation/citation recovery, certify the committee report, or establish general PDF capability. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Exact baseline | Existing MathDevMCP accepts LaTeX paths but has no typed PDF intake; direct `pdftotext` is the naive extraction comparator; the BGS report is a secondary issue inventory, not ground truth. |
| Primary engineering criterion | Unit and interface tests establish source binding, provider binding, bounded response behavior, deterministic normalization, explicit limitations, and graceful unavailable/timeout/malformed-output behavior. |
| Primary audit criterion | Every reported comparison row names a committee anchor, paper/appendix anchor or extraction limitation, classification, rationale, and remaining uncertainty. |
| Hard veto diagnostics | Digest mismatch, provider schema failure, source mutation, missing provenance, no usable parser output, unsupported source claim, or exact-equation claim based only on PDF text. |
| Explanatory-only diagnostics | Parser confidence, parser count, keyword counts, section-heading overlap, generic audit counts, and clean test/build output. |
| Artifact | Adapter source and tests; compact and detailed extraction JSON; source manifest; committee issue inventory; MathDevMCP output; issue comparison matrix; and final report under `docs/reviews/boehl-qe-pdf-audit-2026-07-21/`. |
| Non-claims | No mathematical proof, source certification, exhaustive issue detection, exact PDF-to-LaTeX recovery, committee correctness, paper correctness, or department-release conclusion. |

## External-Tool-First Route

| Tool | Considered role | Selection |
| --- | --- | --- |
| ResearchAssistant | Coordinate `pdftotext`, Marker, GROBID, MinerU, and MarkItDown; reconcile metadata and preserve parser-specific output. | Selected through its stable `scripts/ra-dev parse-pdf` CLI because its current MCP surface does not expose PDF parsing. Do not import its private internals. |
| ResearchAssistant MCP | Direct cross-MCP call. | Not selected for parsing because only parser readiness is exposed; record this capability gap rather than inventing a tool. |
| `pdftotext` | Simple baseline and page/text anchors. | Selected as an explanatory baseline and one ResearchAssistant parser, not as an equation oracle. |
| MathDevMCP LaTeX workflows | Inspect the committee TeX using native labels, neighborhoods, claim-boundary, and focused rigor tools. | Selected for the secondary comparator. |
| SymPy/Sage/Lean | Check a bounded extracted mathematical claim if a faithful formal target and assumptions can be reconstructed. | Conditional only. Do not invoke when PDF extraction cannot preserve the scoped expression. |
| Visual PDF inspection | Resolve formula, table, footnote, or page ambiguity. | Required for material comparison rows whose extracted representation is suspect. |

The adapter is a provider bridge, not a new proof/search algorithm. A future
direct ResearchAssistant MCP parser can replace the transport while preserving
the MathDevMCP response contract.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| ResearchAssistant checkout at `~/python/ResearchAssistant` | User states functions under `~/python` are available. | It is the maintained local provider and exposes a stable development CLI. | Checkout absent, dirty, incompatible, or moved. | Resolve executable, collect git commit/status, call parser matrix. | Reviewed local default, overrideable path required. |
| CLI transport | ResearchAssistant MCP lacks `parse-pdf`. | Avoids importing private implementation. | CLI output or flags drift. | Injected-runner unit tests plus live `--help`/parse smoke. | Baseline transport, not permanent protocol claim. |
| Compact response by default | Existing MathDevMCP MCP responses are bounded. | Multi-parser body text can exceed useful MCP payload size. | Important evidence hidden. | Include per-parser status, lengths/digests, warnings, and an opt-in detailed mode. | Reviewed default. |
| Provider timeout | ResearchAssistant parsers default to 180 seconds each. | Large appendix may require several minutes. | Premature timeout or indefinite run. | Expose bounded adapter timeout and record actual duration/status. | Convenience hypothesis; live run may revise once with reason. |
| Committee report as comparator | User requested comparison to it. | It supplies a concrete issue inventory. | Circular validation or inherited false claims. | Require independent paper/appendix anchors and allow contradiction/not-checked classifications. | Comparator only. |
| Two supplied PDFs | User-selected real-document case. | Paper plus appendix should cover central and technical material. | Published/source version mismatch or OCR artifacts. | Record byte hashes, PDF metadata, filenames, and version limitations. | Fixed case input, not a corpus. |

## Pre-Mortem

The run could appear to pass while misleading us if metadata reconciliation is
good but formulas are corrupted, if large body text is silently truncated, if
the committee report's conclusions are copied into the comparison, or if
generic keyword/notation diagnostics are counted as scientific reproduction.
The earliest checks are per-parser text digests and lengths, manual inspection
of material pages, explicit issue anchors, and a classification rubric that
separates supported matches from parser ambiguity and not-checked rows.

The run could fail for engineering rather than scientific reasons if an
optional parser is unavailable, GROBID is not running, the appendix exceeds a
parser timeout, or the CLI schema has drifted. One optional-parser failure is a
repair trigger, not a continuation veto, provided at least one inspectable
parser output survives and all failures remain visible.

## Phase 1: Typed Provider Bridge

Entry conditions: canonical files exist; both Dynare mission validators pass;
ResearchAssistant CLI and parser contract have been inspected; plan audit below
passes.

Required artifacts:

- a focused `research_assistant_pdf` module with typed validation and injected
  command-runner support;
- a CLI command `extract-pdf-with-research-assistant`;
- an experimental MCP tool `extract_pdf_with_research_assistant` available only
  in the `all` profile;
- unit tests for success, compact/detailed modes, unavailable provider,
  timeout/nonzero exit, malformed JSON/schema, source mutation/binding, and
  stable non-claims;
- interface/count documentation and tests updated consistently.

Checks: focused tests, CLI help/fixture test, facade contract test, stable/all
MCP stdio smoke. Inspect the diff before live parsing.

Handoff condition: the bridge passes tests with an injected provider and one
small local live smoke, without writing outside MathDevMCP.

Stop condition: the only viable implementation requires importing unstable
ResearchAssistant internals, suppressing provider failures, returning
unbounded detail by default, or weakening the source/claim boundary.

## Phase 2: Frozen Source Intake

Entry conditions: Phase 1 passes; source paths and hashes are unchanged.

Required artifacts:

- source/provider manifest with SHA-256, bytes, PDF metadata, git commit/status,
  exact command, environment, CPU/GPU posture, timing, and output paths;
- parser tool matrix;
- compact and detailed extraction JSON for both PDFs;
- direct `pdftotext` baseline files or digest-bound references.

Checks: validate response schemas and digests; compare parser status, text
length, headings, and disagreement; manually inspect first pages and every page
used for a material finding. GPU is intentionally hidden/not used.

Handoff condition: at least one usable extraction exists per PDF and every
parser limitation is retained.

Stop condition: no inspectable text for either PDF, source mutation, or
irreconcilable provider-output corruption.

## Phase 3: Committee And Source Issue Inventories

Entry conditions: Phase 2 source intake is valid.

Required artifacts:

- a scoped inventory of Boehl/QE mathematical issues in the committee TeX with
  line/section/equation anchors;
- a paper/appendix inventory derived independently from extracted text and
  manual PDF inspection;
- focused MathDevMCP reports for source-representable questions, with raw
  diagnostics classified as concrete defect, useful question, low-value or
  duplicate, abstention, or false positive.

Checks: run LaTeX-native indexing/search/neighborhood and claim-boundary tools;
run rigor or backend checks only when the target is faithfully formalized;
verify material PDF quotations/page anchors visually.

Handoff condition: inventories are source-bound and do not silently inherit
the committee verdict.

Stop condition: the report scope cannot be isolated, or a material target
cannot be reconstructed without guessing. Such targets are recorded as not
checked rather than forced through a backend.

## Phase 4: Comparison And Closeout

Entry conditions: both inventories exist with provenance and classifications.

Required artifacts:

- issue matrix using: `supported_match`, `committee_issue_absent_from_source`,
  `source_issue_omitted_by_committee`, `parser_ambiguity_manual_review`,
  `contradiction`, `false_positive_or_low_value`, and `not_checked`;
- final gap report with separate extraction, mathematical-integrity,
  source-fidelity, and rendered-interface ledgers;
- engineering result note covering adapter behavior and remaining direct-MCP
  gap;
- final test and diff record.

Checks: every strong classification has a source anchor; all unsupported or
ambiguous rows remain qualified; focused tests plus the repository test suite
and release/interface checks pass, or failures are precisely recorded.

Completion means the bounded integration and case audit are reproducible. It
does not mean MathDevMCP has general PDF mathematical understanding or that the
Boehl paper or committee report is certified.

## Skeptical Plan Audit

Audit date: 2026-07-21

Verdict: pass after revision.

Problems found and repaired before execution:

1. **Wrong baseline risk:** the first draft implicitly compared only against
   the committee report. Repaired by freezing direct `pdftotext` as the naive
   extraction baseline and treating the committee report as a secondary issue
   inventory rather than truth.
2. **Proxy promotion risk:** parser confidence and generic MathDevMCP finding
   counts could have become success criteria. Repaired by making them
   explanatory only and requiring issue-level source anchors for the audit.
3. **Missing stop condition:** optional parser failure could either halt useful
   work or be silently ignored. Repaired by distinguishing a visible
   single-parser repair trigger from the no-usable-extraction continuation veto.
4. **Hidden source-version assumption:** matching filenames could be mistaken
   for the exact committee-reviewed version. Repaired by recording hashes/PDF
   metadata and retaining version mismatch as a limitation.
5. **Environment mismatch:** `parse-pdf` exists in the ResearchAssistant CLI,
   not its MCP surface. Repaired by selecting the stable CLI behind a typed,
   replaceable provider boundary and explicitly recording the direct-MCP gap.
6. **Artifact inadequacy:** a single prose report would not reveal parser
   truncation or disagreement. Repaired by requiring compact and detailed JSON,
   per-parser digests/lengths, a manifest, inventories, and a comparison matrix.
7. **Stale-context risk:** DynareMCP has an active unrelated readability run.
   Repaired by validating both mission controls and declaring this audit
   separate, read-only work that does not advance or mutate that lane.
8. **Unfair mathematical comparison:** exact equations cannot be recovered
   reliably from PDF text. Repaired by requiring visual/manual reconstruction
   before any backend check and allowing `not_checked` rather than guessing.

The revised commands and artifacts answer the stated questions without crossing
the scientific, publication, shared-worktree, or source-edit boundaries.
