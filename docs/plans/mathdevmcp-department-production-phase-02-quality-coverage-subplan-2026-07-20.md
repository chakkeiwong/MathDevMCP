# P02 Subplan: Quality, Coverage, And Supply Chain

## Objective

Measure executable coverage, establish non-regression floors, add focused
static checks, and produce reproducible dependency evidence.

## Entry Conditions

P01 defines the production surface and installed artifact.

## Required Artifacts

- Coverage/branch configuration and `pytest-cov` development dependency.
- Baseline JSON/XML report and a ratcheted global floor chosen after measurement.
- Higher floors for release, MCP transport/facade, artifact safety, and profile
  policy modules.
- Direct tests for the six modules previously lacking direct imports or a
  documented facade-only exemption.
- Ruff configuration and scoped MyPy gate for new production-boundary modules.
- Runtime constraint file, dependency-inspection/SBOM artifact, and dependency
  vulnerability audit command.
- Explicit fast, integration, external, and full test lanes with duration data.

## Required Checks

- Coverage run with branch data and threshold enforcement.
- Ruff and scoped MyPy.
- Dependency audit and clean `pip check` for the exact department environment.
- Test-lane composition tests; full lane remains authoritative.

## Evidence Contract

The initial coverage percentage is a baseline, not proof of quality. A network
failure in the vulnerability database leaves supply-chain evidence incomplete;
it does not mean no vulnerabilities exist.

## Forbidden Actions

- Do not exclude hard modules merely to inflate coverage.
- Do not add broad `type: ignore`/`noqa` suppressions.
- Do not call the fast lane a release gate.

## Handoff

P03 begins with measurable coverage/static/supply-chain evidence and no silent
unowned production module.

## Stop Conditions

Coverage tooling cannot run reproducibly, or the measured result exposes a
critical untested production boundary that requires characterization first.
