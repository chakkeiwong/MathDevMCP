# Boehl QE Paper/Appendix And Committee Issue Matrix

Date: 2026-07-21

Classification vocabulary follows the execution plan. Line anchors in the
extraction files are navigation evidence; PDF-page inspection is controlling
for mathematical signs and symbols.

| ID | Committee or source issue | Published-source anchor | Committee anchor | Classification | Verdict and boundary |
| --- | --- | --- | --- | --- | --- |
| I01 | Appendix C is not self-executing | Appendix PDF p.17, `appendix-pdftotext-layout.txt:904`--912 | Committee TeX line 17069 | `supported_match` | Correct. The appendix explicitly says flex-price/flex-wage output, premia, leverage, aggregate unconventional-policy measures, notional rate, observables, and steady-state derivations are provided in external YAML/GitHub files. Appendix C alone is not a complete executable contract. |
| I02 | C.52--C.68 require timing/object separation, especially capital accumulation C.59 and return C.62 | Appendix PDF pp.14--15, extraction lines 723--785 | Committee TeX line 17084; reconstructed labels `eq:bgs-c59-level-repeat`, `eq:bgs-c62-level-repeat-ladder` | `supported_match` | Supported as a reconstruction/readability risk, not a demonstrated printed-equation error. The source uses one printed `k_t` notation across installed/effective capital contexts and gives compressed timing. The focused MathDevMCP audit only flagged C.59 as needing formalization; it did not prove a defect. |
| I03 | C.71 liquidity has zero steady state and must be an absolute, not log, deviation | Appendix PDF p.15, extraction lines 796--804 | Committee TeX line 17101; `eq:bgs-c71-level-repeat` | `supported_match` | Correct and explicitly stated by the appendix. A zero steady-state level has no finite log deviation. The separate GDP-scaled observable appears in C.81/C.96, so conflating it with `L^q_t` changes the model. |
| I04 | C.75 positive lagged deposit-return term creates a sign/timing tension | Appendix PDF p.16, C.75; level SDF C.34 on p.11; extraction lines 828--833 and 549--553 | Committee TeX line 17116; `eq:bgs-c75-level-repeat` | `supported_match` | The printed positive term is real. Applying the appendix's stated normalization `(Lambda_t/Lambda_{t-1}) R^d_{t-1}=1` literally gives a negative log movement. The exact source/code timing convention was not independently settled here, so this remains a genuine branch/tension, not a categorical author-error verdict. |
| I05 | C.77 entrant-bank capital uses prior bank-held assets, not total assets | Appendix PDF p.16, C.77; level C.25 on p.9; extraction lines 481--489 and 845--850 | Committee TeX line 17131; `eq:bgs-c77-level-repeat` | `supported_match` | Correct. Both level and linearized printed equations use `K_b` and `B_b`. Replacing them with total stocks adds household/central-bank holdings and is a different transition law. |
| I06 | C.79 long-bond sign and coefficient convention | Appendix PDF p.16, C.79; level return C.47 on p.13; extraction lines 659--668 and 852--862 | Committee TeX line 17144; `eq:bgs-c79-level-ladder` | `supported_match` | Stronger verdict: wrong relative to the appendix's stated target unless an unstated signed-variable convention applies. Differentiating C.47 gives `R^b(r^b_t+q^b_{t-1})=kappa_b Q^b q^b_t`, not the printed negative left side, and C.79 prints fiscal `kappa_tau` rather than bond-price `kappa_b`. The inspected appendix provides no rescue definition. |
| I07 | Post-C.96 full-system commitments are missing from the printed appendix | Appendix PDF p.17, extraction lines 904--912 | Committee TeX line 17153 | `supported_match` | Correct and explicitly admitted by the source. These omissions block unique standalone reconstruction even though they may exist in external code. |
| I08 | Headline effects are approximately -0.9 annual inflation, +8 investment, and -1.2 consumption | Main paper PDF pp.1--2 and conclusion; extraction lines 55--95 and 997--1011 | Committee TeX lines 16858--16866 and author-output replay section | `supported_match` | The values and cost-channel interpretation are visibly reported in the paper. This confirms report fidelity to published claims, not independent causal, estimation, or exact-OBC validation. |
| I09 | Appendix N says `500 x 200 = 10,000` posterior draws | Appendix PDF p.54, extraction lines 2262--2270 | Committee TeX Appendix N discussion, especially lines 16479--16518; absent from final line-17067 inventory | `source_issue_omitted_by_committee` | Concrete arithmetic error: the product is 100,000, consistent with the main paper's p.7 statement. The committee noticed 100,000 as the implied count and a 99,500 captured-backend count, but did not plainly identify the printed 10,000 arithmetic error in its final issue list. |
| I10 | Figure H.8 government-bond-purchase caption says “capital purchases shocks” | Appendix PDF p.27, extraction lines 1256--1265 | No matching defect statement found; report discusses H.7--H.8 reconstruction elsewhere | `source_issue_omitted_by_committee` | Concrete caption defect. The figure title says government bond purchases; the note repeats the H.7 capital-purchase wording. This is editorial/source-fidelity evidence, not a mathematical model refutation. |
| I11 | ResearchAssistant paper metadata reconciliation | Main paper rendered p.1 and compact extraction | No committee analogue | `false_positive_or_low_value` | The provider returns a sentence fragment as title and several headings/fragments as authors. The data are wrong relative to the source. Low confidence/manual review catches risk but does not correct the output. |
| I12 | ResearchAssistant appendix author reconciliation | Appendix PDF metadata; compact extraction | No committee analogue | `false_positive_or_low_value` | Title is correct, authors are wrong. PDF metadata already contains the correct authors, but the parser route does not use it effectively. |
| I13 | MathDevMCP seven-label focused rigor result | `committee-focused-rigor-audit.*` | Seven source-bound committee labels | `false_positive_or_low_value` | It returned one generic C.59 `needs_formalization` issue, no concrete repair, and did not surface I03--I07. Useful localization and abstention, but low issue recall and poor prioritization for this real-document task. |
| I14 | Exact structural lower-bound/counterfactual validity | Main paper method and counterfactual pages; committee's extensive OBC/code evidence | Committee final scientific gate | `not_checked` | The two PDFs state the method and results but cannot establish exact solver/counterfactual validity. This audit did not execute author code, replay masks, estimate the model, or reproduce the posterior. Committee claims in this lane are therefore comparator context, not revalidated here. |

## Reproduction Summary

Of the seven final paper/appendix issues at committee lines 17069--17160, all
seven are supported at the stated reconstruction boundary. Six are explicit
source facts or tensions (I01, I03--I07); I02 is a supported timing/notation
risk rather than a proved error. I06 admits the strongest mathematical verdict:
the printed C.79 relation differs from the first-order movement of its own C.47
level target.

The audit also finds two simple appendix defects not stated plainly in the
final committee issue list: I09 and I10. No committee issue was contradicted.
The exact-OBC, posterior, code, and counterfactual validity claims remain not
checked by this PDF-focused run.
