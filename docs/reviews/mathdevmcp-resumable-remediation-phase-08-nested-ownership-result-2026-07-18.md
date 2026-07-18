# Nested-Alignment Ownership Diagnostic Result

Date: 2026-07-18

Status: `TYPED_ABSTENTION_RETAINED`

## Question

Can the seven frozen D447 lookup-only labels be promoted to unambiguous,
byte-bound mathematical row or display ownership?

## Source Binding

- file: `bgs_final_committee_report_d447.tex`
- SHA-256: `c5cfc66061ce90b053cf7e1df6eb770bababfcda85aa54c26546437037da0690`
- source repository: DynareMCP, read-only

## Tool Ledger

| Tool | Version/status | Role | Decision |
| --- | --- | --- | --- |
| MathDevMCP current locator | `p02_lightweight_locator@1` | exact byte/source lookup | selected authority; retains all seven labels as `nested_display_ownership_required` |
| LaTeXML | 0.8.6 | independent transformed-structure diagnostic | diagnostic only; localized all seven but supplied no exact source-byte ownership |
| SymPy/SageMath | available | algebra/calculus | not applicable to TeX row ownership |
| Lean and proof-state tools | available/partial | certification after formalization | not applicable before source ownership and formalization |

LaTeXML completed in approximately 88 seconds with 36 warnings and one
malformed-structure error elsewhere in the document. Its XML distinguished the
three branch labels as separate `equation` nodes and the four grouped labels as
separate labeled `equationgroup` nodes. The generated XML rewrites node IDs and
does not bind those nodes to exact source byte spans.

## Label Ledger

| Label | Current exact-source state | LaTeXML diagnostic | Decision |
| --- | --- | --- | --- |
| `eq:branch-l64a` | label after first sibling inner `aligned` block | distinct equation node | retain abstention |
| `eq:branch-l64b` | label after second sibling inner `aligned` block | distinct equation node | retain abstention |
| `eq:branch-l64c` | label after third sibling inner `aligned` block | distinct equation node | retain abstention |
| `eq:s08-gk-direct-holdings-budget` | outer suffix after one multi-row `aligned` block | labeled equation group | retain abstention |
| `eq:s08-gk-eq35-eq37-retail-calvo` | outer suffix after one multi-row `aligned` block | labeled equation group | retain abstention |
| `eq:s08-gk-eq38-eq40-policy` | outer suffix after one multi-row `aligned` block | labeled equation group | retain abstention |
| `eq:s08-gk-eq42-eq45-equilibrium` | outer suffix after one multi-row `aligned` block | labeled equation group | retain abstention |

## Decision

The promotion condition did not pass. Independent structural agreement is
useful localization evidence, but it is not one exact documented source-span
ownership rule with byte evidence. Promoting the four grouped labels would also
require deciding whether a label owns every relation in its grouped display;
promoting the three branch labels requires a reviewed sibling-inner-environment
span rule. Those are parser/oracle changes, not facts established by LaTeXML.

The seven `nested_display_ownership_required` statuses remain correct,
actionable typed abstentions. No source or index implementation was changed.

## Non-Claims

- LaTeXML localization is not mathematical proof or source-byte ownership.
- Retained abstention is not a refutation of any displayed equation.
- This diagnostic does not establish that a future reviewed ownership rule is
  impossible.
