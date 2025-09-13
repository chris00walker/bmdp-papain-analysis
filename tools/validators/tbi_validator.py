#!/usr/bin/env python3
"""
TBI Validator
Validates Testing Business Ideas (TBI) rigor: assumptions, evidence, and learning integration.

Usage:
  python tools/tbi_validator.py --business businesses/grower --validate [area]

Notes:
- Designed to be called by workspace rules and workflows.
- Safe by default: analysis only; no file mutations.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path


def validate_tbi(business_path: Path, area: str | None = None) -> dict:
    """Stub validator for TBI rigor.

    Returns a result dict with status and messages. Placeholder to implement
    assumption mapping, evidence quality, and learning loop checks.
    """
    result = {
        "business": business_path.name,
        "area": area or "all",
        "status": "ok",
        "messages": [
            "TBI validation placeholder executed.",
            "Implement assumption, evidence, and learning checks here.",
        ],
        "score_estimate": 0.0,
    }

    # Minimal file presence checks commonly used in understand/design
    indicative = [
        ("20_understand", "assumption_testing.md"),
        ("20_understand", "evidence_ledger.csv"),
    ]
    missing = []
    for d, f in indicative:
        if not (business_path / d / f).exists():
            missing.append(f"{d}/{f}")
    if missing:
        result["status"] = "warn"
        result["messages"].append(f"Missing indicative files: {', '.join(missing)}")

    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TBI validator")
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

    result = validate_tbi(business_path, area=args.validate)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"[TBI] business={result['business']} area={result['area']} status={result['status']}")
        for msg in result["messages"]:
            print(f" - {msg}")

    return 0 if result["status"] in {"ok", "warn"} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
