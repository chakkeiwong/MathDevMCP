#!/usr/bin/env python3
"""Write a release manifest for a built MathDevMCP wheel."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mathdevmcp.release_artifacts import build_release_manifest, write_release_manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dependency-lock", type=Path)
    parser.add_argument("--tests", type=Path, help="Optional JSON test summary bound to an artifact_path")
    args = parser.parse_args()
    tests = json.loads(args.tests.read_text(encoding="utf-8")) if args.tests else None
    manifest = build_release_manifest(args.root, args.wheel, dependency_lock=args.dependency_lock, test_summary=tests)
    write_release_manifest(manifest, args.output)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
