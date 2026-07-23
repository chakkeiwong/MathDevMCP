# Fresh R4 Run Manifest

| field | value |
| --- | --- |
| classification | tuned replay; not blind holdout |
| access boundary | noncompliant: prior plan/result artifacts were inspected before execution; see `replay-report.md` |
| command | `PYTHONPATH=src python -m mathdevmcp.cli audit-applied-math-document <paper.pdf> <appendix.pdf> --mode reproduce --specialist-policy none --response-mode detailed --artifact-root docs/reviews/boehl-qe-tuned-replay-2026-07-22/fresh-r4` |
| input count | 2 PDFs; no code; no data |
| exit status | 0 |
| artifact | `audit-fcd0847c98b84e3de119b2977abacf3e.json` |
| artifact SHA-256 | `6a8955037b86f120354b2438d39cc9da2de7635c220e98601522bb0e90afa86d` |
| CLI capture SHA-256 | `60691b3e7040d583684de19a8efc8cfbd98571398b5af84eff246e333c0d1e1d` |
| MathDevMCP revision | `c192dab6cc4b6d35e02f8f056f6ec3e47d3ba2c7` |
| environment | `/home/chakwong/miniconda3/envs/tfgpu/bin/python`, Python 3.11.15 |
| GPU | not requested or used |
| provider | ResearchAssistant local CLI, commit `3e9315eb52cf23166e913dfa2566d1908d18f45b`, dirty worktree reported |
| usable parser | `/usr/bin/pdftotext`, Poppler 22.02.0; one parser per PDF |
| specialist execution | none (`specialist-policy=none`) |
| findings | 11 diagnostic `supported_tension`; 0 promoted defects |
| claim IR validation | no errors |

The detailed JSON artifact and exact stdout capture are colocated with this
manifest. All conclusions are bounded by the access and non-claim statements in
`replay-report.md`.
