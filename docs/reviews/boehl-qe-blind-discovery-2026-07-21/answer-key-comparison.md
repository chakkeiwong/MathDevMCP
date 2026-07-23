# Blind Boehl PDF Discovery: Answer-Key Comparison

Date: 2026-07-21

## Freeze And Isolation Status

The discovery report and run manifest were frozen before this comparison was
started:

| Artifact | SHA-256 |
| --- | --- |
| `blind-discovery.md` | `5bf66d4d3384871dbc11acb73404b9913486f3bb1407b00f153fe91e0ddcb6b8` |
| `blind-run-manifest.md` | `a9f9940659d9709b7431da497c2dcb98d2a8e837844fc351d485a7148acdc689` |

The run is **content-isolated but not pristine**. An initial `git status
--short` exposed the names of the forbidden prior plan/review paths. It did not
expose their contents, issue labels, locations, issue count, or conclusions,
and the fresh agent reports that it never opened or searched them. The path
names could reveal that a prior Boehl audit existed, but they do not explain any
answer-key item. Results below are therefore usable as a qualified blind case
study, not as a perfect isolation experiment.

The answer key is the seven-item final paper/appendix inventory already
source-checked against the PDFs. It is not treated as proof of the paper's
global validity or as an exhaustive defect list.

## Answer-Key Matching

| Key | Answer-key issue | Frozen blind match | Match | Provenance and scoring reason |
| --- | --- | --- | --- | --- |
| K01 | Appendix C is not self-executing | `INF-11` | `exact` | Agent inference from MathDevMCP-transported PDF evidence. It explicitly identifies the external YAML dependency and inability to reconstruct the full model from the PDF. |
| K02 | C.52--C.68 require timing/object separation, especially C.59/C.62 | None | `missed` | `INF-10` finds a different `h gamma` versus `h/gamma` defect within the same equation range. It does not identify the installed/effective-capital or return-timing issue in the answer key. |
| K03 | C.71 has zero steady state and therefore uses an absolute, not log, deviation | Abstention text only | `partial` | The fresh agent noticed the PDF's zero-steady-state statement and tried `assumptions-for 'log(L)'`, then correctly reported that the public route failed to flag positivity. It did not promote the reconstruction constraint into its findings list. |
| K04 | C.75 deposit-return sign/timing tension | None | `missed` | C.75 was rendered and transcribed, but the blind report contains no sign/timing finding for it. |
| K05 | C.77 entrant capital uses bank-held rather than total assets | None | `missed` | The blind report transcribes C.77 but does not compare the ownership domain with total asset stocks. |
| K06 | C.79 conflicts with C.47 in sign and coefficient | `INF-09` | `exact` | Agent inference from MathDevMCP-transported evidence. It independently compares C.47 and C.79 and identifies both the sign and `kappa_b`/`kappa_tau` conflict. |
| K07 | Required full-system equations after C.96 are outside the PDF | `INF-11` | `exact` | Same blind finding as K01. K01 and K07 are separate entries in the answer key but share one semantic discovery. |

Descriptively, the fresh-agent workflow produced **3 exact, 1 partial, and 3
missed answer-key matches**. Exact item recall is `3/7` (42.9%). Counting any
partial recognition without pretending it is an exact finding gives coverage
of `4/7` items (57.1%). One discovery (`INF-11`) accounts for two overlapping
answer-key entries, so these item counts represent only two distinct exact
discovery topics: completeness and C.79.

## Attribution

| Lane | Answer-key result | Interpretation |
| --- | --- | --- |
| ResearchAssistant PDF extraction | `0/7` findings | It transported one-parser text and warnings. It emitted no paper-defect findings. |
| Autonomous public MathDevMCP findings | `0/7` | No public function independently selected and emitted an answer-key issue. |
| MathDevMCP backend checks after agent localization | Two non-answer-key checks | SymPy confirmed the Appendix N arithmetic mismatch and the M.15 counterexample only after the agent selected and encoded the claims. These are verification, not autonomous discovery. |
| Fresh Codex agent using MathDevMCP evidence | 3 exact, 1 partial, 3 missed | All answer-key recognition came from agent semantic reasoning over transported PDF evidence. |
| Direct PDF inspection lane | `0/7` new matches | Page rendering confirmed agent-localized notation; the one separately attributed direct finding concerned blank main-PDF metadata. |

The frozen report's provenance label `raw_mathdevmcp_finding` means that a
public backend explicitly returned a mismatch for the encoded expressions. For
the discovery question, that label is too generous: the agent first had to
find, transcribe, and formulate both candidates. The tool discovered neither
candidate autonomously.

## Findings Outside The Seven-Item Answer Key

The blind report promoted fourteen unmatched findings. Bounded source and
render checks found no promoted false positive, but these findings have
different scientific weight:

| Class | Blind IDs | Evaluation |
| --- | --- | --- |
| Closed printed arithmetic/algebra defects | `RAW-01`, `RAW-02` | Source-supported. The posterior multiplication is false; M.15 uses the reciprocal of the ratio implied by M.14. This does not establish what author code executed. |
| Cross-display equation inconsistencies | `INF-01`, `INF-05`, `INF-07`, `INF-08`, `INF-10`, `INF-12` | Source-supported literal conflicts involving discounting, coefficient identity, timing, first-order terms, detrending, or domain restrictions. Code impact remains not checked. |
| Notation/definition/interface defects | `INF-02`, `INF-03`, `INF-04`, `INF-06`, `INF-13` | Source-supported notation, sector-description, aggregation, or statistical-terminology defects. They range from substantive reconstruction barriers to editorial errors. |
| PDF metadata interface | `DIR-01` | `pdfinfo` confirms blank standard title/author fields for the main PDF. This is a document-interface defect, not a mathematical finding. |

`RAW-01` was also found in the earlier human-assisted audit but was not one of
the committee report's seven final paper/appendix items. The remaining unmatched
claims are additions relative to that seven-item answer set; this evaluation
does not claim they are absent from every section of the much larger committee
report.

## False Positives And Abstentions

No promoted blind finding was rejected in the bounded source check. This is not
a precision estimate: the corpus contains one document pair and some findings
would need source code to determine implementation impact.

The run did expose a concrete MathDevMCP numeric-tolerance false positive. A
corrected M.15 positive control left a floating residual of about
`-6.94e-18`, which `check-proof-obligation` labeled `mismatch`. The fresh agent
correctly abstained. It also rejected generic `derive-or-refute` counterexamples
whose supplied assumptions were not enforced and reported that
`assumptions-for` failed to surface the positivity requirement for a logarithm
under a supplied zero-steady-state statement.

## Verdict

This test is revealing but does not show that MathDevMCP discovers the report's
errors. The current PDF bridge supplied source text and provenance; the fresh
Codex agent supplied the successful cross-equation reasoning. Even with that
agent, three answer-key items were missed and one was only noticed as an
abstention. The strongest positive evidence is that an answer-key-isolated
agent independently found C.79 and the non-self-contained model boundary, while
also finding several plausible additional printed defects.

The next repair target is not broader prompting. It is a measurable
extraction-to-audit pipeline that creates page/equation objects, compares level
and linearized equation pairs, checks steady-state/domain/timing/ownership
contracts, detects external specification dependencies, and preserves every
candidate or abstention in a compact report.

## Non-Claims

- no general PDF precision or recall estimate;
- no paper, code, posterior, OBC, likelihood, or counterfactual certification;
- no claim that backend verification equals autonomous issue discovery;
- no claim that every unmatched finding affects executed author code;
- no claim that the qualified filename-listing deviation is equivalent to a
  pristine blind run.
