#!/usr/bin/env python3
"""Minimal structural check. Does not validate scientific correctness."""
from pathlib import Path
import json

root = Path(__file__).resolve().parent.parent
required = [
    "README.md", "AGENTS.md", "LICENSE", "docs/methodology.md",
    "research/HYP-0001.md", "experiments/EXP-0001/manifest.json",
    "wiki/Home.md", "crates/ci-core/src/lib.rs",
]
for name in required:
    if not (root / name).is_file():
        raise SystemExit(f"missing required artifact: {name}")
manifest = json.loads((root / "experiments/EXP-0001/manifest.json").read_text())
assert manifest["status"] == "planned" and manifest["results"] is None
print("Research structure valid; no claim of scientific or Rust verification.")
