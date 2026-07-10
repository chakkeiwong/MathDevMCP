from __future__ import annotations

"""Structured agent-hypothesis expansions for derivation-tree blockers."""

from dataclasses import asdict, dataclass
from typing import Any

from .contracts import attach_contract


AGENT_HYPOTHESIS_EXPANSION_CONTRACT = "agent_hypothesis_expansion"
AGENT_HYPOTHESIS_EXPANSION_SET_CONTRACT = "agent_hypothesis_expansion_set"
AGENT_HYPOTHESIS_BOUNDARY = (
    "Agent hypotheses are candidate branch expansions only. They are not "
    "repairs, proofs, validated assumptions, or backend certificates until the "
    "derivation tree records certifying or blocking evidence."
)

ALLOWED_EXPECTED_BACKENDS = {
    "sympy",
    "sage",
    "lean",
    "leandojo",
    "pantograph",
    "leansearchv2",
    "source_evidence",
    "manual_formalization",
    "human_review",
}


@dataclass(frozen=True)
class AgentHypothesisExpansion:
    id: str
    target_blocker_id: str
    blocker_kind: str
    proposed_route: str
    assumptions_added: list[str]
    why_might_close: str
    expected_backend: str
    expected_backend_role: str
    success_criterion: str
    failure_criterion: str
    source_refs: list[str]
    provenance: str = "agent_generated_candidate"
    status: str = "candidate_pending_tree_verification"
    boundary: str = AGENT_HYPOTHESIS_BOUNDARY


def _text(value: Any) -> str:
    return " ".join(str(value or "").split())


def _slug(value: Any) -> str:
    text = _text(value).lower()
    chars = [char if char.isalnum() else "_" for char in text]
    return "_".join("".join(chars).split("_")) or "hypothesis"


def _source_refs(blocker: dict[str, Any], source_context: dict[str, Any] | None = None) -> list[str]:
    refs = [str(item) for item in blocker.get("evidence_refs", []) if str(item)]
    if source_context:
        for key in ("id", "label", "location"):
            if source_context.get(key):
                refs.append(str(source_context[key]))
    return list(dict.fromkeys(refs))


def _candidate(
    blocker: dict[str, Any],
    *,
    route_id: str,
    proposed_route: str,
    assumptions_added: list[str],
    why_might_close: str,
    expected_backend: str,
    expected_backend_role: str,
    success_criterion: str,
    failure_criterion: str,
    source_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blocker_id = _text(blocker.get("id"))
    kind = _text(blocker.get("kind"))
    payload = asdict(
        AgentHypothesisExpansion(
            id=f"agent_hypothesis_{_slug(blocker_id)}_{route_id}",
            target_blocker_id=blocker_id,
            blocker_kind=kind,
            proposed_route=proposed_route,
            assumptions_added=assumptions_added,
            why_might_close=why_might_close,
            expected_backend=expected_backend,
            expected_backend_role=expected_backend_role,
            success_criterion=success_criterion,
            failure_criterion=failure_criterion,
            source_refs=_source_refs(blocker, source_context),
        )
    )
    return attach_contract(payload, AGENT_HYPOTHESIS_EXPANSION_CONTRACT)


def validate_agent_hypothesis_expansion(expansion: dict[str, Any]) -> list[str]:
    """Validate one candidate expansion without certifying its mathematics."""
    errors: list[str] = []
    metadata = expansion.get("metadata")
    if not isinstance(metadata, dict) or metadata.get("contract") != AGENT_HYPOTHESIS_EXPANSION_CONTRACT:
        errors.append(f"metadata.contract must be {AGENT_HYPOTHESIS_EXPANSION_CONTRACT}")
    required_text_fields = [
        "id",
        "target_blocker_id",
        "blocker_kind",
        "proposed_route",
        "why_might_close",
        "expected_backend",
        "expected_backend_role",
        "success_criterion",
        "failure_criterion",
        "provenance",
        "status",
        "boundary",
    ]
    for field in required_text_fields:
        if not _text(expansion.get(field)):
            errors.append(f"{field} must be a non-empty string")
    assumptions = expansion.get("assumptions_added")
    if not isinstance(assumptions, list) or not [_text(item) for item in assumptions if _text(item)]:
        errors.append("assumptions_added must contain at least one non-empty assumption")
    if _text(expansion.get("expected_backend")) not in ALLOWED_EXPECTED_BACKENDS:
        errors.append("expected_backend is not an allowed backend or evidence route")
    if _text(expansion.get("provenance")) != "agent_generated_candidate":
        errors.append("provenance must be agent_generated_candidate")
    if _text(expansion.get("status")) != "candidate_pending_tree_verification":
        errors.append("status must be candidate_pending_tree_verification")
    boundary = _text(expansion.get("boundary")).lower()
    if "not" not in boundary or "proof" not in boundary:
        errors.append("boundary must explicitly state the hypothesis is not proof")
    for field in ("proposed_route", "why_might_close", "success_criterion", "failure_criterion"):
        if len(_text(expansion.get(field)).split()) < 4:
            errors.append(f"{field} is too vague")
    return errors


def hypothesis_expansion_errors(expansions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return validation errors indexed by expansion id."""
    results: list[dict[str, Any]] = []
    for expansion in expansions:
        if not isinstance(expansion, dict):
            results.append({"id": "<non-dict>", "errors": ["expansion must be a dict"]})
            continue
        errors = validate_agent_hypothesis_expansion(expansion)
        if errors:
            results.append({"id": str(expansion.get("id", "<missing>")), "errors": errors})
    return results


def propose_hypothesis_expansions(
    blocker: dict[str, Any],
    *,
    source_context: dict[str, Any] | None = None,
    typed_obligation: dict[str, Any] | None = None,
    failed_paths: list[dict[str, Any]] | None = None,
    max_candidates: int = 3,
) -> dict[str, Any]:
    """Create deterministic seed hypotheses for a blocker.

    This function is the schema boundary for later LLM-generated hypotheses.
    Today it emits conservative deterministic routes from blocker kinds, then
    validates them before a tree search can consume them.
    """
    kind = _text(blocker.get("kind"))
    blocker_id = _text(blocker.get("id"))
    failed_ids = {
        _text(item.get("id") or item.get("hypothesis_id"))
        for item in failed_paths or []
        if isinstance(item, dict)
    }
    candidates: list[dict[str, Any]] = []
    if kind == "conditional_law_translation_required":
        candidates.extend(
            [
                _candidate(
                    blocker,
                    route_id="finite_support_law",
                    proposed_route="Rewrite the conditional expectation as a finite weighted sum under an explicit finite support law.",
                    assumptions_added=[
                        "The conditioned shock or next-state object has finite support.",
                        "Conditional probabilities for each support point are defined and sum to one.",
                    ],
                    why_might_close="A finite support law replaces the abstract conditional expectation with a finite algebraic sum that SymPy or Sage can inspect.",
                    expected_backend="sympy",
                    expected_backend_role="certify scoped finite-sum algebra after translation",
                    success_criterion="The translated finite weighted sum is algebraically equal to the target branch expression.",
                    failure_criterion="Block if the support, weights, or random payoff values cannot be specified as finite backend symbols.",
                    source_context=source_context,
                ),
                _candidate(
                    blocker,
                    route_id="kernel_integrability_law",
                    proposed_route="Introduce a typed conditional kernel and integrability assumptions before attempting a Lean formalization.",
                    assumptions_added=[
                        "A conditional kernel for the random object is fixed.",
                        "Every payoff term is measurable and has finite conditional first moment under the kernel.",
                    ],
                    why_might_close="A typed kernel and integrability route makes the conditional expectation a well-defined mathematical object before certification.",
                    expected_backend="lean",
                    expected_backend_role="check a manually formalized scoped theorem after the kernel and assumptions are encoded",
                    success_criterion="Direct Lean checking accepts the scoped theorem without placeholders under the explicit kernel assumptions.",
                    failure_criterion="Block if the kernel, sigma-field, or integrability assumptions cannot be encoded explicitly.",
                    source_context=source_context,
                ),
            ]
        )
    elif kind == "conditioning_scope_translation_required":
        candidates.extend(
            [
                _candidate(
                    blocker,
                    route_id="sigma_field_scope",
                    proposed_route="Declare the conditioning object as a sigma-field or information set and rewrite the conditional expectation relative to that object.",
                    assumptions_added=[
                        "The conditioning object is a sigma-field, information set, or state variable with a defined generated sigma-field.",
                        "Every random term inside the conditional expectation is measurable relative to the ambient probability space.",
                    ],
                    why_might_close="A backend or formal proof needs the conditional bar to name an actual conditioning object rather than a typographical separator.",
                    expected_backend="source_evidence",
                    expected_backend_role="verify or cite the local definition of the conditioning object before formalization",
                    success_criterion="The source or proposed assumption identifies the conditioning object and its mathematical role unambiguously.",
                    failure_criterion="Block if the conditioning object could be a state, sigma-field, information set, or kernel argument with no disambiguating evidence.",
                    source_context=source_context,
                ),
                _candidate(
                    blocker,
                    route_id="kernel_argument_scope",
                    proposed_route="Treat the conditioning object as the argument of a conditional transition kernel and bind the kernel to the expectation.",
                    assumptions_added=[
                        "A conditional transition kernel is defined at the conditioning object.",
                        "The random variables inside the expectation are distributed according to that kernel.",
                    ],
                    why_might_close="A kernel argument route makes the conditioning scope explicit enough for Lean or manual formalization.",
                    expected_backend="lean",
                    expected_backend_role="check a scoped theorem after the kernel argument and measurability assumptions are encoded",
                    success_criterion="Direct Lean checking accepts the scoped theorem with the kernel argument encoded explicitly.",
                    failure_criterion="Block if no kernel or transition law can be tied to the conditioning object.",
                    source_context=source_context,
                ),
            ]
        )
    elif kind == "integrability_translation_required":
        candidates.append(
            _candidate(
                blocker,
                route_id="bounded_envelope",
                proposed_route="Postulate a dominated-envelope or finite-first-moment condition for every random payoff term.",
                assumptions_added=[
                    "Each random payoff term is measurable under the conditional law.",
                    "Each random payoff term is dominated by an integrable envelope or has finite conditional first moment.",
                ],
                why_might_close="The expectation becomes finite only after the random terms have integrability evidence.",
                expected_backend="source_evidence",
                expected_backend_role="verify or cite the missing integrability condition before backend translation",
                success_criterion="A source citation or explicit assumption closes the typed integrability blocker.",
                failure_criterion="Block if no source citation or explicit integrability assumption is available.",
                source_context=source_context,
            )
        )
    elif kind == "derivative_expectation_interchange_required":
        candidates.extend(
            [
                _candidate(
                    blocker,
                    route_id="finite_state_derivative_sum",
                    proposed_route="Replace the conditional expectation by a finite sum and differentiate the finite sum term by term.",
                    assumptions_added=[
                        "The conditional law has finite support independent of the differentiated choice variable.",
                        "Each payoff derivative in the finite support sum exists.",
                    ],
                    why_might_close="Finite sums allow term-by-term differentiation without invoking a dominated convergence or Leibniz interchange theorem.",
                    expected_backend="sympy",
                    expected_backend_role="check the resulting finite symbolic derivative after the expectation is translated to a sum",
                    success_criterion="The differentiated finite-sum expression matches the target first-order condition algebraically.",
                    failure_criterion="Block if the support, weights, or payoff derivatives cannot be represented as finite symbolic terms.",
                    source_context=source_context,
                ),
                _candidate(
                    blocker,
                    route_id="dominated_leibniz_interchange",
                    proposed_route="Add a dominated derivative envelope and use a Leibniz or dominated convergence interchange theorem.",
                    assumptions_added=[
                        "The payoff derivative exists almost surely in a neighborhood of the choice.",
                        "The derivative is dominated by an integrable envelope under the conditional law.",
                    ],
                    why_might_close="A dominated envelope supplies the missing mathematical condition for moving the derivative inside the expectation.",
                    expected_backend="lean",
                    expected_backend_role="check a manually formalized scoped interchange theorem after assumptions are encoded",
                    success_criterion="Direct Lean checking accepts the scoped interchange theorem under the dominated-envelope assumptions.",
                    failure_criterion="Block if the derivative envelope, neighborhood, or conditional law cannot be stated explicitly.",
                    source_context=source_context,
                ),
            ]
        )
    elif kind == "choice_independent_transition_law_required":
        candidates.append(
            _candidate(
                blocker,
                route_id="law_independence",
                proposed_route="State that the conditional transition law is independent of the differentiated choice variable before differentiating.",
                assumptions_added=[
                    "The conditional transition law does not vary with the differentiated choice variable.",
                    "Any dependence of future shocks on the choice is absent or explicitly accounted for by kernel-derivative terms.",
                ],
                why_might_close="Without law independence, differentiating an expectation can create omitted derivatives of the transition kernel.",
                expected_backend="source_evidence",
                expected_backend_role="verify or cite the transition-law independence assumption before backend translation",
                success_criterion="Source evidence or an explicit assumption states the law independence condition for the scoped FOC.",
                failure_criterion="Block if the law may depend on the choice and no kernel-derivative terms are included.",
                source_context=source_context,
            )
        )
    elif kind == "missing_domain_or_shape_required":
        candidates.append(
            _candidate(
                blocker,
                route_id="domain_shape_declarations",
                proposed_route="Add explicit scalar, vector, matrix, and conformability declarations before backend translation.",
                assumptions_added=[
                    "Every symbol in the target has a declared domain and mathematical role.",
                    "Every matrix or vector product has conformable dimensions.",
                ],
                why_might_close="Algebra and proof backends need domain and shape declarations to distinguish legal products from ill-typed expressions.",
                expected_backend="manual_formalization",
                expected_backend_role="produce a typed symbol and dimension map before backend execution",
                success_criterion="Every backend symbol has a domain and all products or transposes have conformable dimensions.",
                failure_criterion="Block if any symbol role or dimension remains ambiguous.",
                source_context=source_context,
            )
        )
    elif kind == "macro_translation_required":
        candidates.append(
            _candidate(
                blocker,
                route_id="symbol_map",
                proposed_route="Build a typed symbol map from every LaTeX macro in the target to backend variables or definitions.",
                assumptions_added=[
                    "Each LaTeX macro used in the target has a declared mathematical type.",
                    "Each declared macro has a backend-safe symbol name or definition.",
                ],
                why_might_close="Backend execution needs typed symbols rather than document-only macro names.",
                expected_backend="manual_formalization",
                expected_backend_role="produce the symbol map required before SymPy, Sage, or Lean execution",
                success_criterion="Every macro in the blocker has a typed backend symbol or a declared unsupported construct blocker.",
                failure_criterion="Block if any macro remains untyped or maps ambiguously to more than one mathematical object.",
                source_context=source_context,
            )
        )
    elif kind == "grouped_multiline_obligation_required":
        candidates.append(
            _candidate(
                blocker,
                route_id="split_or_group_rows",
                proposed_route="Group all localized rows into one formal obligation or split them into smaller labeled obligations before backend checking.",
                assumptions_added=[
                    "Every row in the multiline display belongs to the same derivation chain or is assigned a separate label.",
                    "Each split obligation has explicit left-hand side, right-hand side, and justification.",
                ],
                why_might_close="A backend cannot certify an arbitrary row from a multiline display unless the full obligation or each split step is defined.",
                expected_backend="manual_formalization",
                expected_backend_role="produce scoped backend targets for the grouped display or for each split row",
                success_criterion="The multiline display is represented as one complete formal target or as separately checkable labeled obligations.",
                failure_criterion="Block if row boundaries or equality-chain semantics remain ambiguous.",
                source_context=source_context,
            )
        )
    elif kind == "full_display_source_required":
        candidates.append(
            _candidate(
                blocker,
                route_id="recover_display_source",
                proposed_route="Recover the complete LaTeX display environment and use it as the source span for formalization.",
                assumptions_added=[
                    "The complete display source is available with begin and end environment and labels.",
                    "The localized row is mapped back to the full display without losing surrounding terms.",
                ],
                why_might_close="Repair and backend targets need the full mathematical expression, not a row fragment.",
                expected_backend="source_evidence",
                expected_backend_role="recover exact source span before any backend execution or report edit",
                success_criterion="The target packet includes complete display source and source line span.",
                failure_criterion="Block if the display cannot be recovered uniquely from the LaTeX file.",
                source_context=source_context,
            )
        )
    elif kind in {"accounting_identity_condition", "valuation_condition", "counterfactual_condition"}:
        candidates.append(
            _candidate(
                blocker,
                route_id="finite_horizon_accounting_identity",
                proposed_route="Formalize the finite-horizon accounting identity by declaring baseline path, action path, exhaustive components, signs, discount factors, and terminal value.",
                assumptions_added=[
                    "Baseline and action paths are defined on the same horizon and information set.",
                    "Listed cash-flow components are exhaustive and share one sign convention.",
                    "Discount factors and terminal value are finite and defined for the horizon.",
                ],
                why_might_close="Once all finite-horizon accounting objects are defined, the remaining equality can be reduced to scoped algebraic aggregation.",
                expected_backend="sympy",
                expected_backend_role="check the finite aggregation algebra after the accounting objects are symbol mapped",
                success_criterion="The backend verifies that the component aggregation equals the displayed finite-horizon identity under the stated symbol map.",
                failure_criterion="Block if any component, sign convention, horizon, or terminal-value definition is missing.",
                source_context=source_context,
            )
        )
    else:
        candidates.append(
            _candidate(
                blocker,
                route_id="manual_formalization",
                proposed_route="Split the blocker into an explicit typed obligation and ask for the smallest backend-checkable subclaim.",
                assumptions_added=[
                    "The blocked claim is restated as a scoped typed obligation.",
                    "Any assumptions needed by the scoped obligation are listed before backend execution.",
                ],
                why_might_close="A smaller typed obligation may isolate the exact construct that prevents backend checking.",
                expected_backend="manual_formalization",
                expected_backend_role="prepare the next backend-checkable target or exact blocker",
                success_criterion="The blocker is replaced by a backend formalization target or a more specific blocker.",
                failure_criterion="Block if the claim cannot be decomposed into a scoped typed obligation.",
                source_context=source_context,
            )
        )
    filtered = [candidate for candidate in candidates if candidate.get("id") not in failed_ids][: max(0, int(max_candidates))]
    validation_errors = hypothesis_expansion_errors(filtered)
    status = "candidate_expansions_ready" if filtered and not validation_errors else "invalid_or_empty_candidate_expansions"
    payload = {
        "status": status,
        "target_blocker_id": blocker_id,
        "blocker_kind": kind,
        "candidate_count": len(filtered),
        "candidates": filtered,
        "validation_errors": validation_errors,
        "typed_obligation_id": typed_obligation.get("id") if isinstance(typed_obligation, dict) else None,
        "boundary": AGENT_HYPOTHESIS_BOUNDARY,
        "non_claims": [
            "Agent hypotheses are not repairs.",
            "Agent hypotheses are not proof certificates.",
            "Tree/backend validation is required before a hypothesis can support report text.",
        ],
    }
    return attach_contract(payload, AGENT_HYPOTHESIS_EXPANSION_SET_CONTRACT)
