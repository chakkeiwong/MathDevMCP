# Boehl QE Tuned Replay Report

## Scope and result

This was an instruction-compliant tuned replay, not a blind holdout. The public MathDevMCP CLI audited only the supplied main paper PDF and appendix PDF. It completed with status `completed_with_limits` and wrote the detailed JSON artifact at `audit-bb3f727858d91340.json`. The CLI reported SHA256 `44623c704f609eabdd82ddec1d621b971678f0523f0d38a2d61b432912946dbb`; the final on-disk path was observed at SHA256 `7263c1114de840e8a9316314ac5321efdd212212f2037e70ad1486f66d322163`, indicating a concurrent shared-workspace rewrite after the CLI returned. Both digests are recorded in the manifest.

The run emitted 13 finding records: one CLI-labeled `confirmed_defect` (high severity) and 12 `supported_tension` records (medium severity). These are diagnostic outputs from PDF extraction and relationship checks, not a claim of general recall, source-faithful equation recovery, or mathematical correctness.

## Findings emitted

1. High, `confirmed_defect`: the extracted text reports `500 x 200 = 10,000`; the arithmetic check reports that `500*200 = 100,000`.
2. Medium, `supported_tension`: required equations/model objects are supplied externally, so the document is not self-contained for reconstruction.
3. Medium, `supported_tension`: uncertainty displays use both confidence-interval and credible-set terminology without a consistently stated statistical target.
4. Medium, `supported_tension`: a zero steady state is combined with log-deviation language; an absolute-deviation convention or positive-level condition is needed.
5. Medium, `supported_tension`: the zero steady state of central-bank liquidity injections and the stated level/log deviation convention require explicit checking.
6. Medium, `supported_tension`: a level return relation and its linearized movement require differentiation and coefficient/sign verification.
7. Medium, `supported_tension`: the entrant-stock relation uses an asset-ownership domain that must be checked rather than replaced with aggregate holdings.
8. Medium, `supported_tension`: model closure depends on an external equation package; standalone reconstruction is incomplete until that package is inspected.
9-13. Medium, `supported_tension`: five candidate level/linearized equation pairs require explicit expansion-point, order, sign, coefficient, timing, and domain comparisons.

## Limitations and non-claims

- ResearchAssistant extraction was `extracted_with_manual_review` for both PDFs, with `low` parse confidence and only `pdftotext` usable. `marker`, `grobid`, `mineru`, and `markitdown` were unavailable or failed; no multi-parser consensus was established.
- PDF equations and normalized objects are non-certifying. The high-severity arithmetic item is the CLI's extracted-text classification and still warrants checking against the rendered source before publication or correction.
- No code paths or data paths were provided, so implementation alignment and numerical reproduction were not checked. No specialist backend was executed.
- The ResearchAssistant checkout was dirty at the reported provider commit, so the commit does not uniquely identify the exact provider worktree.
- Six of the 12 selected obligations were unresolved/not checkable in the generated coverage record; obligation coverage does not solve those obligations or prove the paper wrong.
- This single document case cannot establish general error-detection recall or precision, scientific validity, causal conclusions, publication readiness, or a default-policy decision.

## Access statement

To the best of the operator's knowledge, no comparator, answer key, committee report, prior report, plan, or other review artifact was accessed. The replay used only the two input PDFs and the public CLI. This is an instructional/self-reported boundary, not OS-enforced isolation.
