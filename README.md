# MathDevMCP

MathDevMCP is a proposed internal toolchain for mathematical software development, large-scale LaTeX documentation, code-document consistency checking, and Claude Code MCP integration.

The initial repository contains a detailed LaTeX project proposal in `docs/` and a minimal implementation scaffold in `src/mathdevmcp/`.

## Agent guides

- [Operator guide](docs/mathdevmcp-operator-guide.md) explains the general paper-reading and code-grounding workflow.
- [Kalman Hessian guide](docs/kalman-hessian-agent-guide.md) gives practical discipline for analytical Kalman-filter Hessian derivations.

## Build the proposal

```bash
cd docs
pdflatex -interaction=nonstopmode -halt-on-error proposal.tex
bibtex proposal
pdflatex -interaction=nonstopmode -halt-on-error proposal.tex
pdflatex -interaction=nonstopmode -halt-on-error proposal.tex
```

## Run scaffold tests

```bash
python -m pytest tests -q
```

## Current status

This is an early project scaffold. The first implementation focus is a LaTeX/document indexing layer plus simple CLI commands that can later be exposed through MCP tools.
