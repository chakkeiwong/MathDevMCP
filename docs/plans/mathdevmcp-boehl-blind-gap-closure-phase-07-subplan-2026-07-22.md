# Phase 07 Subplan: Instruction-Compliant Tuned Replay

Objective: run the unchanged PDFs once in a fresh session and compare only
after freezing the output; test fresh-user discoverability, not generalization.

Entry: Phase 06 implementation/prompt/manifests frozen.

Artifacts: replay report, manifest, audit artifact, post-hoc comparison, result.

Checks/review: input digests, self-reported access declaration, attribution,
scoring, false-
positive review, remaining gaps.

Evidence: same-paper result is descriptive and tuned, not a system holdout;
filesystem isolation and non-access are self-reported, not enforced evidence.

Forbidden: answer-key content in the prompt, input changes, blind/system-
holdout or leakage-sensitive claims, or rerun after comparison.

Handoff: exact/partial/missed and regression status are frozen.

Stop: leakage, source drift, or missing artifact.
