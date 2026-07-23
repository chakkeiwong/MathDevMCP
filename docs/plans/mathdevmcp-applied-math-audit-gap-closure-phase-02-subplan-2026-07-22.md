# Phase 02 Subplan: Claim IR And Dependency Graph

## Objective

Represent mathematical objects and their explicit or uncertain relationships so
checks can operate on relationships rather than a flat keyword stream.

## Entry Conditions

Phase 01 packets validate and retain source anchors.

## Required Artifacts

Versioned IR builders/validators, graph records, cross-domain fixtures, and a
Phase 02 result.

## Required Checks/Tests/Reviews

Check deterministic IDs, source-span conservation, explicit LaTeX reference
edges, ambiguous-adjacency edges, unresolved references, cycles, and compact /
detailed round trips.

## Evidence Contract

Every node and edge stores source references, extraction tier, confidence, and
whether the relation is explicit, inferred, or unresolved.

## Forbidden Claims/Actions

Keyword similarity and physical adjacency cannot establish dependency or a
scientific claim.

## Exact Handoff Conditions

Validators can receive a graph and distinguish explicit edges from candidates;
all unresolved edges remain visible.

## Stop Conditions

Stop if raw evidence is lost or graph construction silently drops unresolved
relationships.
