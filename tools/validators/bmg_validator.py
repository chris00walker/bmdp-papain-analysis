#!/usr/bin/env python3
"""
BMG Validator
Validates Business Model Generation (BMG) nine building blocks coherence.

Usage:
  python tools/bmg_validator.py --business businesses/grower --validate [area]

Notes:
- Designed to be called by workspace rules and workflows.
- Safe by default: analysis only; no file mutations.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path


def validate_bmg(business_path: Path, area: str | None = None) -> dict:
    """Stub validator for BMG coherence.

    Returns a result dict with status and messages. This is a placeholder
    implementation to be expanded with real checks (canvas, blocks coherence,
    viability alignment, etc.).
    """
    result = {
        "business": business_path.name,
        "area": area or "all",
        "status": "ok",
        "messages": [
            "BMG validation placeholder executed.",
            "Implement nine building blocks coherence checks here.",
        ],
        "score_estimate": 0.0,
    }

    # Minimal sanity checks for expected directories
    required_dirs = ["10_mobilize", "20_understand", "30_design"]
    missing = [d for d in required_dirs if not (business_path / d).exists()]
    if missing:
        result["status"] = "warn"
        result["messages"].append(f"Missing expected directories: {', '.join(missing)}")

    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="BMG nine building blocks validator")
    parser.add_argument("--business", required=True, help="Path to business root (e.g., businesses/grower)")
    parser.add_argument("--validate", nargs="?", const="all", default="all", help="Validation area or 'all'")
    parser.add_argument("--format", choices=["json", "summary"], default="summary")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    business_path = Path(args.business).resolve()
    if not business_path.exists():
        print(f"Error: business path not found: {business_path}", file=sys.stderr)
        return 2

    result = validate_bmg(business_path, area=args.validate)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"[BMG] business={result['business']} area={result['area']} status={result['status']}")
        for msg in result["messages"]:
            print(f" - {msg}")

    return 0 if result["status"] in {"ok", "warn"} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
