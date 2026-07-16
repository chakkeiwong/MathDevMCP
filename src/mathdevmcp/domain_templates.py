"""Governed diagnostic templates for recurring math-finance obligations."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract


@dataclass(frozen=True)
class DomainTemplate:
    id: str
    domain: str
    description: str
    assumptions: list[str]
    supported_notation: list[str]
    generated_obligations: list[str]
    diagnostic_routes: list[str]
    failure_modes: list[str]
    positive_fixtures: list[str]
    negative_fixtures: list[str]
    certification_boundary: str


TEMPLATES: tuple[DomainTemplate, ...] = (
    DomainTemplate(
        id="valuation_terminal_value_v1",
        domain="bounded_terminal_value_definition",
        description="Source-bound scalar terminal-value placeholder with explicit persistence and decay denominator.",
        assumptions=["claim role is source-evidenced as a definition", "terminal-value denominator is explicitly nonzero", "scalar symbols have declared real-valued meaning"],
        supported_notation=["terminal value", "persistence", "attrition", "discount rate", "decay", "continuation cash flow"],
        generated_obligations=["source definition role", "exact nonzero denominator", "algebraic cross-multiplication consistency", "terminal-value sensitivity remains an external scientific obligation"],
        diagnostic_routes=["claim_semantics", "assumption_discovery", "sympy", "proof_packet"],
        failure_modes=["definition treated as a theorem", "zero denominator", "terminal value treated as economic truth", "policy or expectation semantics silently simplified"],
        positive_fixtures=["eq:terminal-value-base"],
        negative_fixtures=[],
        certification_boundary="This diagnostic template can check source role, scalar algebra, and denominator domain only; it cannot certify economic validity, calibration, policy optimality, or a universal terminal-value theorem.",
    ),
    DomainTemplate(
        id="valuation_finite_horizon_dcf_v1",
        domain="finite_horizon_discounted_cash_flow",
        description="Finite-horizon discounted cash-flow accounting with explicit acquisition cost and terminal term.",
        assumptions=["horizon is finite and nonnegative", "discount factors and timing convention are declared", "each cash-flow term is finite", "conditional laws and integrability are declared when expectations occur"],
        supported_notation=["NPV", "finite horizon", "discount factor", "cash flow", "acquisition cost", "terminal value"],
        generated_obligations=["finite aligned horizon", "discount timing", "cash-flow and terminal-term finiteness", "conditional-law and integrability review", "source claim role"],
        diagnostic_routes=["claim_semantics", "assumption_discovery", "finite_support_expectation", "proof_packet"],
        failure_modes=["infinite or mismatched horizon", "unstated discount convention", "unsupported conditional expectation", "causal or policy semantics mistaken for algebra"],
        positive_fixtures=["eq:incremental-npv"],
        negative_fixtures=[],
        certification_boundary="The template generates diagnostic obligations and must abstain on unsupported expectation, causal, behavioral, and policy semantics; it is not a valuation-validity certificate.",
    ),
    DomainTemplate(
        id="kalman_loglikelihood_v1",
        domain="filtering_state_space",
        description="Gaussian prediction-error likelihood with solve/logdet diagnostics.",
        assumptions=["innovation covariance is SPD", "dimensions are conformable", "observations follow linear Gaussian measurement equation"],
        supported_notation=["logdet", "innovation", "solve", "covariance"],
        generated_obligations=["logdet domain", "linear solve residual", "quadratic form shape", "prediction-error decomposition"],
        diagnostic_routes=["matrix_ir", "shape_diagnostics", "numeric_diagnostics"],
        failure_modes=["missing SPD assumption", "missing conformability", "unsupported nonlinear observation equation"],
        positive_fixtures=["eq:dept-state-space-likelihood"],
        negative_fixtures=["eq:proof-audit-false"],
        certification_boundary="Template output is diagnostic until each generated obligation is backend-certified.",
    ),
    DomainTemplate(
        id="cip_sdf_sign_v1",
        domain="affine_cip_sdf",
        description="CIP/SDF sign-convention reconciliation.",
        assumptions=["FX quote convention is explicit", "domestic and foreign discount factors are defined", "basis sign convention is registered"],
        supported_notation=["forward", "spot", "basis", "SDF", "discount factor"],
        generated_obligations=["quote convention", "basis sign convention", "no-arbitrage pricing identity"],
        diagnostic_routes=["convention_registry", "dependency_graph", "proof_packet"],
        failure_modes=["missing convention", "ambiguous positive basis sign", "missing discount-factor definition"],
        positive_fixtures=[],
        negative_fixtures=[],
        certification_boundary="Template output is diagnostic until convention-specific obligations are backend-certified.",
    ),
    DomainTemplate(
        id="hmc_transform_jacobian_v1",
        domain="posterior_geometry_hmc",
        description="Transform density, Jacobian correction, and HMC acceptance obligations.",
        assumptions=["transform is differentiable", "Jacobian determinant has valid domain", "target density support is respected"],
        supported_notation=["Jacobian", "logdet", "acceptance", "Hamiltonian", "transform"],
        generated_obligations=["change of variables", "log-Jacobian correction", "finite target", "acceptance ratio identity"],
        diagnostic_routes=["matrix_ir", "numeric_diagnostics", "proof_packet"],
        failure_modes=["missing differentiability", "invalid transform support", "surrogate evidence mistaken for exact correction"],
        positive_fixtures=["eq:dept-hmc-leapfrog"],
        negative_fixtures=[],
        certification_boundary="Template output is diagnostic until each generated obligation is backend-certified.",
    ),
)


def list_domain_templates() -> dict:
    return attach_contract(
        {
            "status": "consistent",
            "reason": "Domain templates are available.",
            "templates": [asdict(template) for template in TEMPLATES],
        },
        "domain_template_catalog",
    )


def suggest_domain_templates(*, label: str = "", section_path: list[str] | None = None, equation_text: str = "") -> dict:
    haystack = " ".join([label, " ".join(section_path or []), equation_text]).lower()
    matches: list[dict] = []
    for template in TEMPLATES:
        terms = [template.domain, template.description, *template.supported_notation]
        score = sum(1 for term in terms if term.lower() in haystack)
        if score:
            item = asdict(template)
            item["score"] = score
            matches.append(item)
    matches.sort(key=lambda item: (-item["score"], item["id"]))
    return attach_contract(
        {
            "status": "suggested" if matches else "inconclusive",
            "reason": "Domain templates matched the supplied context." if matches else "No domain template matched the supplied context.",
            "matches": matches,
        },
        "domain_template_suggestions",
    )


def generate_obligations_from_template(template_id: str, *, label: str) -> dict:
    template = next((item for item in TEMPLATES if item.id == template_id), None)
    if template is None:
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": f"Unknown domain template: {template_id}",
                "template_id": template_id,
                "obligations": [],
                "actions": [{"kind": "choose_supported_template", "severity": "medium"}],
            },
            "domain_template_obligations",
        )
    obligations = [
        {
            "id": f"{template.id}:{index}",
            "label": label,
            "description": description,
            "required_assumptions": template.assumptions,
            "status": "unverified",
            "substatus": "unverified:manual_formalization_required",
            "certification_boundary": template.certification_boundary,
        }
        for index, description in enumerate(template.generated_obligations, start=1)
    ]
    return attach_contract(
        {
            "status": "unverified",
            "reason": "Template obligations were generated as diagnostic review tasks.",
            "template": asdict(template),
            "obligations": obligations,
        },
        "domain_template_obligations",
    )
