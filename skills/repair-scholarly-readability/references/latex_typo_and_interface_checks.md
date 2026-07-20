# LaTeX Typo And Interface Checks

## Deterministic Checks

Run the bundled surface auditor and the repository's normal LaTeX build. Check:

- duplicate labels and missing reference targets;
- important unlabeled displays and numbered equations never referenced;
- undefined citations and references in the build log;
- overfull/underfull boxes and clipped or split displays;
- repeated words, placeholders, and punctuation-spacing candidates;
- heading hierarchy, abstract length, contents depth, and figure/table counts;
- PDF page count, extracted-text availability, and rendered-page output.

These are candidates for inspection. TeX macros and mathematical notation can
produce false positives.

## Human Typo Audit

Read rendered text beside the source. Inspect:

- author names, years, titles, acronyms, and capitalization;
- minus signs, primes, hats, bars, subscripts, superscripts, and transpose marks;
- equation numbering and prose references;
- singular/plural agreement around mathematical objects;
- matrix orientation, index order, and supplier/user language;
- inconsistent hyphenation and terminology;
- malformed quotations, dashes, nonbreaking spaces, and citations;
- source typos that should be reported rather than silently corrected.

## Rendered Interface Audit

Inspect contact sheets for global density and individual pages at readable
resolution. Check:

- whether the first page states the puzzle and document purpose;
- whether the abstract is a summary rather than an audit ledger;
- whether a long document offers clear reading routes;
- whether headings reveal an argument rather than only source inventory;
- whether boxes, tables, and figures carry meaning instead of decoration;
- whether equations have enough surrounding explanation;
- whether page breaks separate a claim from its qualifier;
- whether tables, captions, footnotes, and hyperlinks are legible;
- whether whitespace and paragraph length create a usable rhythm.

## Interpretation Boundary

A clean log proves only that LaTeX completed under the selected command. A low
warning count, short abstract, or visually attractive page does not establish
comprehension, mathematical correctness, source fidelity, or scientific value.
