#!/usr/bin/env python3
"""Validate a manifest and required paths without reading raw file contents."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from spatial_pipeline.manifest import load_manifest, validate_required_paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=ROOT / "data/sample_manifest.csv")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    frame = load_manifest(args.manifest)
    missing = validate_required_paths(frame, args.root)
    development = int((frame["split"] == "development").sum())
    final_test = int((frame["split"] == "final_test").sum())
    print(f"samples={len(frame)} development={development} final_test={final_test}")
    if missing:
        print(f"missing_paths={len(missing)}")
        for item in missing:
            print(item)
        return 1
    print("manifest and required paths are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
