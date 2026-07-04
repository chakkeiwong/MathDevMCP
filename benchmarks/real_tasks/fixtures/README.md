# Normalized candidate-answer fixtures

This directory contains **normalized candidate-answer fixtures** for the
real-task benchmark structural scorer.

These fixtures are not model outputs and not semantic free-form answers. They
are small, explicit candidate objects that exercise the current deterministic
structural scoring layer against committed public benchmark cases.

Each fixture should record:

- the target `case_id`,
- a normalized answer object,
- and the expected structural scoring outcome for that fixture.

The purpose of these fixtures is to make structural scoring reproducible before
any richer semantic answer-to-candidate layer exists.
