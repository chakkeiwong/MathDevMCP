# Fresh Codex Blind Boehl Run: Post-Hoc Comparison

Date: 2026-07-22

## Protocol

The blind report and audit artifact were frozen before this comparison was
opened. The fresh session received only the two supplied PDFs and used the
public `audit-applied-math-document` CLI. It did not inspect the committee
report, answer key, prior Boehl reviews, or plan files. This file is a
post-hoc comparison and is not part of the blind agent input.

Inputs:

* Main PDF SHA-256: `bb3f727858d9134064235753a783947756e32f7dbc65a7a177886cab5dc5fd29`
* Appendix PDF SHA-256: `c02de9858a64ddc39d7499ed8a83bae28442941041894082f16bca44cabe4052`
* Frozen audit artifact SHA-256: `22edf0efc28a0ae512da44da2345e6f42977229e5036a3774babe4a76563c8c0`

## Fresh-Run Output

The fresh report contains 13 findings:

* 1 `confirmed_defect`: Appendix N reports `500 x 200 = 10,000`; the correct
  product is `100,000`.
* 12 `supported_tension` findings: external model closure, uncertainty
  terminology, zero/log boundary, level/linearization boundaries, return
  derivation, entrant ownership domain, several equation-pair obligations,
  and the conditional non-ZLB impulse-response interpretation.
* 6 selected obligation families remain `not_checkable` because no code, YAML,
  data, or certifying backend was supplied.

## Comparison With The Seven-Item Committee Inventory

| Committee issue | Fresh blind outcome | Classification | Reason |
| --- | --- | --- | --- |
| I01: Appendix C is not self-executing | F2 and F8 | exact topic | The fresh report explicitly identifies the external GitHub/YAML equation dependency and incomplete standalone reconstruction. |
| I02: C.52--C.68 timing/object separation, especially C.59/C.62 | F9, with related F10/F13 | partial | The fresh report identifies C.59 and the surrounding level/linearization obligation, but does not independently identify the precise installed/effective-capital and C.62 return-timing reconstruction. |
| I03: C.71 zero steady state requires absolute deviation | F4 and F5 | exact topic | The fresh report states that zero liquidity cannot have a finite log deviation and requires an explicit absolute-deviation convention. |
| I04: C.75 deposit-return sign/timing tension | No direct C.75 finding | missed | The fresh report discusses adjacent SDF/linearization obligations but does not identify the printed positive lagged deposit-return sign/timing tension. |
| I05: C.77 uses bank-held, not total, assets | F7 | partial | The fresh report preserves the bank-held ownership domain and warns against aggregate-stock substitution, but does not independently assert the committee's exact C.77 correction. |
| I06: C.79 sign and coefficient conflict with C.47 | F6 | partial | The fresh report nominates the C.47-to-linearized-return derivation and coefficient/sign check, but does not reach the committee's stronger wrong-relative-to-target verdict. |
| I07: equations after C.96 are outside the PDF | F2 and F8 | exact topic | The same external-equation finding explicitly establishes the missing full-system closure. |

## Score

Using the issue-level vocabulary from the prior benchmark:

* 2 exact topics / 7 inventory items, because one external-closure finding maps
  to both I01 and I07;
* 3 partial items: I02, I05, I06;
* 1 missed item: I04;
* I03 is an exact topic match, so the item-level result is **3 exact, 3
  partial, 1 missed**.

This is a semantic comparison of a fresh agent report against the frozen
inventory. It is not a population recall estimate. The repeated external
closure topic is counted separately at the inventory-item level and as one
topic at the discovery-topic level.

## Attribution

The public tool artifact autonomously emitted the arithmetic defect and
source-supported tensions. The fresh Codex session selected, grouped, and
explained those records in the blind report. It did not execute author code,
inspect YAML, derive the C.75/C.79 relations to a certifying standard, or
validate posterior/causal/numerical claims.

## Interpretation

The fresh run is materially more informative than the earlier answer-key-
informed regression because it preserves the answer-key boundary. It shows that
the repaired orchestrator can autonomously surface several relevant source and
relationship obligations, including the C.71 boundary and C.77 ownership
domain. It still misses the C.75 sign/timing issue and does not prove the
stronger C.79 conflict. The dominant remaining limitation is semantic
formalization of paired equations, not PDF intake or report transport.

## Non-Claims

This comparison does not certify the paper, code, posterior, likelihood, ZLB
solution, impulse responses, causal interpretation, or scientific conclusions.
It does not establish general precision/recall or prove that unmatched issues
are absent from the documents.
