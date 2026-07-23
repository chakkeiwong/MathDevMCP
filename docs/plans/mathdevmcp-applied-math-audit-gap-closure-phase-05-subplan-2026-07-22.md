# Phase 05 Subplan: Claim Evidence And Paging

## Objective

Expose a versioned, artifact-backed evidence chain that an LLM can page without
losing source fidelity or non-claims.

## Entry Conditions

Packets, graph, validators, and route records exist.

## Required Artifacts

Claim IR schema/version, evidence resolver, compact projection, paging records,
CLI/facade/server tests, and Phase 05 result.

## Required Checks/Tests/Reviews

Verify compact/detail parity, bounded payloads, deterministic page tokens,
tamper detection, exact record resolution, and non-claim propagation.

## Evidence Contract

Every finding resolves source -> object -> edge -> check -> result; unresolved
links remain explicit.

## Forbidden Claims/Actions

Do not hide unresolved detail behind counts or allow mutable paths to act as
authority.

## Exact Handoff Conditions

One compact finding handle resolves to its exact immutable detailed record.

## Stop Conditions

Stop if compact output cannot resolve detail or artifact integrity fails.
