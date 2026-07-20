# Department Operations Record

Status: `owner_and_corpus_authority_required`

This status is a release blocker until the department assigns the product,
release/build, and security/privacy owners below. A passing test or project-
owner review cannot infer those authorities.

## Supported Boundary

The supported deployment is a trusted local stdio process launched by an
authorized colleague. Do not expose it as a network service or process hostile
documents. The stable MCP profile is the default; experimental and deprecated
tools require `MATHDEVMCP_MCP_PROFILE=all` and a supervised change record.

## Ownership And Escalation

| Responsibility | Assigned owner | Status |
| --- | --- | --- |
| Department product owner | To be assigned by department | External authority required |
| Release/build maintainer | To be assigned by department | External authority required |
| Mathematical/scientific reviewer | Project owner | Existing supervision boundary |
| Security/privacy approver | To be assigned by department | External authority required |

Until the first two rows are assigned, this document is an operational template,
not evidence of support ownership.

## Rollback And Incident Procedure

1. Stop the local MCP process and preserve the release manifest and redacted
   logs.
2. Reinstall the previously approved wheel identified by its manifest SHA-256.
3. Re-run the stable-profile stdio smoke and `pip check`.
4. Escalate mathematical-status, private-data, or schema-contract incidents to
   the project owner before modifying source or deleting evidence.
5. Retain manifests, test summaries, and incident records according to the
   department retention policy once that policy is assigned.

No rollback rehearsal can be declared complete until a department owner binds
an approved previous wheel and retention destination.
