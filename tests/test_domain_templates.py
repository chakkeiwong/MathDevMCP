from mathdevmcp.domain_templates import generate_obligations_from_template, list_domain_templates, suggest_domain_templates


def test_domain_template_catalog_declares_governance_fields():
    catalog = list_domain_templates()

    assert catalog["metadata"] == {"schema_version": "1.0", "contract": "domain_template_catalog"}
    template = catalog["templates"][0]
    for field in [
        "assumptions",
        "supported_notation",
        "generated_obligations",
        "diagnostic_routes",
        "failure_modes",
        "positive_fixtures",
        "negative_fixtures",
        "certification_boundary",
    ]:
        assert field in template
    assert "diagnostic" in template["certification_boundary"].lower()


def test_suggest_domain_templates_matches_equation_context():
    suggestions = suggest_domain_templates(
        label="eq:dept-state-space-likelihood",
        section_path=["Filtering and likelihood"],
        equation_text="logdet innovation covariance solve",
    )

    assert suggestions["status"] == "suggested"
    assert suggestions["matches"][0]["id"] == "kalman_loglikelihood_v1"


def test_generate_template_obligations_remains_unverified():
    result = generate_obligations_from_template("hmc_transform_jacobian_v1", label="eq:hmc")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "domain_template_obligations"}
    assert result["status"] == "unverified"
    assert result["obligations"]
    assert {item["status"] for item in result["obligations"]} == {"unverified"}
