# ResearchAssistant-Backed Boehl QE PDF Audit: Final Gap Report

Date: 2026-07-21

## Outcome

ResearchAssistant helps materially with PDF intake, but the current combined
system does not accomplish MathDevMCP's mission for PDF-only mathematical
documents without substantial human reasoning.

The successful part is engineering: MathDevMCP now has an experimental,
source-bound provider bridge that invokes ResearchAssistant without importing
its internals, hashes the input, records provider identity and parser status,
preserves capability limits, fails closed on malformed output/source mutation,
and returns compact output by default. Both supplied PDFs were parsed and all
artifacts are reproducible from the manifest.

The unsuccessful part is scientific automation: only `pdftotext` was available;
ResearchAssistant produced wrong semantic metadata; equation/citation structure
remained unreliable; and the focused MathDevMCP rigor audit missed six of the
seven committee issues despite receiving exact relevant labels. The meaningful
comparison required manual rendered-page inspection, an independently built
issue inventory, and one hand-specified SymPy discriminator.

## Main Findings

1. **The committee's seven final paper/appendix issues reproduce.** Appendix C
   is not self-executing; C.52--C.68 are timing/notation sensitive; C.71
   explicitly uses an absolute liquidity deviation; C.75 contains the reported
   positive deposit-return tension; C.77 uses bank-held assets; C.79 contains a
   sign/coefficient conflict; and post-C.96 full-system equations are delegated
   outside the PDF.
2. **C.79 is wrong relative to its stated level target.** Appendix C.47 defines
   `R^b_t=(xi+kappa_b Q^b_t)/Q^b_{t-1}`. Its first-order movement has a
   positive left side and `kappa_b`. Printed C.79 negates the left side and
   uses `kappa_tau`, which C.46/C.78 define as fiscal feedback. No inspected
   source definition reconciles those objects.
3. **C.75 is not resolved as categorical error.** The printed positive term
   conflicts with the literal log movement of the stated deposit normalization,
   but exact dating/code normalization was not independently closed. The direct
   verdict is `unsupported branch choice`, not proof that the authors' intended
   executable equation is wrong.
4. **Two additional appendix defects were found.** Appendix N prints
   `500 x 200 = 10,000`, not 100,000. Figure H.8 is a government-bond
   purchase comparison whose note says capital purchases. The committee had a
   sophisticated Appendix N replication discussion but did not state these two
   literal defects in its final paper/appendix issue inventory.
5. **The paper's headline numbers are source-faithful.** The PDFs visibly report
   about -0.9 percent annual inflation, nearly +8 percent investment, and about
   -1.2 percent consumption. This audit does not validate the causal or exact
   structural interpretation.

## Remaining Product Gaps

### ResearchAssistant Integration

| Gap | Evidence | Needed repair |
| --- | --- | --- |
| No PDF parse MCP tool | Provider documents and adapter transport record | Expose a read-only, bounded `ra_parse_pdf` MCP tool or a versioned provider protocol so MathDevMCP need not shell through the CLI. |
| One usable parser only | Both compact packets list only `pdftotext` | Make optional-parser installation/readiness explicit; add a calibrated fallback ladder rather than presenting reconciliation as multi-parser when only one output exists. |
| Wrong title/authors | Main paper title is a sentence fragment; both author lists are wrong | Use PDF metadata and front-page layout as high-priority candidates; validate author/title candidates; attach per-field confidence and abstain rather than emit obvious fragments. |
| No structured equation/page objects | Capability matrix marks equations/citations unreliable | Emit page-bounded text blocks with page numbers, bounding boxes when available, formula-image references, parser provenance, and uncertainty. Do not claim LaTeX recovery. |
| Dirty provider identity not exact | ResearchAssistant has unrelated untracked build files | Add provider-code content identity or a narrow tracked-source digest; git commit plus dirty flag is diagnostic but not exact provenance. |
| CLI schema is implicit | Adapter validates a dataclass-shaped JSON without a provider schema/version field | Add a ResearchAssistant response schema version and compatibility contract. |

### MathDevMCP Mathematical Detection

| Gap | Evidence | Needed repair |
| --- | --- | --- |
| PDF workflows stop at extraction | New bridge returns text/metadata but cannot route page/equation objects | Add an extraction-to-audit work packet with page anchors, source images, candidate equations, assumptions, and explicit formalization status. |
| Low issue recall for supplied labels | Seven-label rigor audit found only generic C.59 formalization | Add cross-equation consistency checks for level-vs-linearized identities, sign conventions, timing, units/zero steady state, symbol collisions, and ownership/stock decomposition. |
| No document-completeness detector | Post-C.96 delegation was found by reading prose, not the rigor tool | Detect explicit external-equation/code dependencies and report standalone-reconstruction gaps. |
| No comparator-inventory workflow | Human had to translate committee prose into seven source questions | Add a typed claim/issue inventory importer and issue-by-issue source comparison with `supported`, `contradicted`, `not found`, and `not checkable` results. |
| Detailed payload is disproportionate | 706 KB JSON for seven labels, one generic issue | Make compact the default for CLI as well as MCP, expose paged detailed evidence, and report a utility summary tied to the requested issue classes. |
| Actionable Markdown drops relevant source facts | 1.3 KB report includes only C.59 | Preserve source-confirmed resolutions and missed requested issue classes, not only generated open issues. |
| Backend routing needs explicit targets | SymPy helped only after a human encoded C.79 | Add level-to-first-order template generation and typed symbol/steady-state assumptions; never infer economic target from OCR alone. |

### Audit And Scientific Limits

| Gap | Status |
| --- | --- |
| Exact OBC solution validity | Not checked; requires author code/same-object solver evidence, not PDF extraction. |
| Posterior and convergence validity | Not checked; Appendix N text and plots are insufficient. |
| Counterfactual structural validity | Not checked; headline values are reported and committee replay context exists, but this run did not reproduce estimation/solution. |
| Citation correctness/exhaustiveness | Not checked; ResearchAssistant explicitly marks PDF citations unreliable. |
| General PDF capability | Unsupported; this is one paper/appendix pair with selectable text. |

## Four-Ledger Closeout

| Ledger | Verdict |
| --- | --- |
| Reader comprehension | The final matrix makes the seven committee findings, two newly localized source defects, and non-checked lanes decidable. The raw generated reports do not: the detailed rigor JSON is too large and the compact Markdown omits most requested issue classes. |
| Mathematical integrity | C.79 received a scoped source-plus-SymPy verdict; C.71/C.77 are direct source facts; C.75 remains an unresolved sign/timing branch; exact OBC, posterior, and full-model validity are not checked. |
| Source fidelity | Input hashes, PDF pages, parser output, rendered-page inspection, and committee line anchors are preserved. Wrong ResearchAssistant metadata was rejected rather than silently reused. |
| Typography/rendering | Main paper pp.1--2 and appendix pp.15--17 were rendered and inspected. No clipping or equation-rendering defect was observed there; source typos/signs were visible in the PDF itself. The entire 77-page pair was not visually audited page by page. |

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Keep the ResearchAssistant bridge as experimental | Source/provider binding and focused interface tests pass | No engineering veto | Provider CLI schema and dirty-worktree identity | Stabilize provider schema/MCP parse surface and add page-aware equation packets | General PDF readiness |
| Accept the seven committee PDF findings at their stated boundaries | Each has a rendered/source anchor | No contradiction found | C.75 executable convention and all code-dependent claims | Preserve C.75 as branch; repair/clarify C.79 in any reconstruction | Paper globally wrong |
| Do not promote current PDF audit workflow | Human work was essential and automated issue recall was poor | Promotion veto fired | Multi-parser/formula extraction and semantic audit recall | Build benchmark fixtures from I01--I13 before further algorithm repair | Mission accomplished for PDFs |

## Post-Run Red Team

The strongest alternative explanation for the poor automated result is that
the tool was aimed at the committee's reconstructed equations rather than a
native structured source of the paper. That explains some abstention but not
the failure to use the supplied surrounding prose to surface zero-steady-state,
bank-held-asset, and convention conflicts. The weakest evidence is C.75 because
the executable timing normalization was not checked against author code. A
source package or code witness that explicitly defines a signed `r^d` or
different `M_t` timing could overturn that branch interpretation. It would not
repair the literal C.79 coefficient/sign mismatch without another explicit
definition.

The next smallest discriminating program is a regression corpus containing the
two bad ResearchAssistant metadata cases, C.71/C.75/C.77/C.79/post-C.96, the
Appendix N arithmetic error, and H.8 caption mismatch. Repairs should be scored
on issue-level precision/recall and abstention quality, not raw diagnostic count.
