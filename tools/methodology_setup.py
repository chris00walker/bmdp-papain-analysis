#!/usr/bin/env python3
"""
Methodology Setup
Initializes framework scaffolding or verifies prerequisites for methodology validation.

Usage:
  python tools/methodology_setup.py --business businesses/grower [--apply]

Notes:
- Safe by default: performs checks only. Use --apply to perform non-destructive
  setup actions (e.g., creating missing folders). Script is idempotent.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path


def check_prerequisites(business_path: Path) -> dict:
    """Check minimal directory structure and key files exist."""
    required_dirs = ["00_initiation", "10_mobilize", "20_understand", "30_design"]
    missing_dirs = [d for d in required_dirs if not (business_path / d).exists()]

    required_files = [
        ("30_design", "financials_cashflow.csv"),
        ("20_understand", "evidence_ledger.csv"),
    ]
    missing_files = [f"{d}/{f}" for d, f in required_files if not (business_path / d / f).exists()]

    return {
        "business": business_path.name,
        "status": "ok" if not missing_dirs and not missing_files else "warn",
        "missing_dirs": missing_dirs,
        "missing_files": missing_files,
    }


def apply_setup(business_path: Path, plan: dict) -> list[str]:
    """Optionally create missing non-contentious directories.

    Does NOT create content files to avoid overwriting user work.
    """
    actions = []
    for d in plan.get("missing_dirs", []):
        target = business_path / d
        target.mkdir(parents=True, exist_ok=True)
        actions.append(f"created: {target}")
    return actions


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Methodology setup and prerequisite checks")
    parser.add_argument("--business", required=True, help="Path to business root")
    parser.add_argument("--apply", action="store_true", help="Apply safe, idempotent setup actions")
    parser.add_argument("--format", choices=["json", "summary"], default="summary")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    business_path = Path(args.business).resolve()
    if not business_path.exists():
        print(f"Error: business path not found: {business_path}", file=sys.stderr)
        return 2

    plan = check_prerequisites(business_path)
    actions: list[str] = []
    if args.apply:
        actions = apply_setup(business_path, plan)

    if args.format == "json":
        print(json.dumps({"plan": plan, "actions": actions}, indent=2))
    else:
        print(f"[SETUP] business={plan['business']} status={plan['status']}")
        if plan["missing_dirs"]:
            print(f" - missing dirs: {', '.join(plan['missing_dirs'])}")
        if plan["missing_files"]:
            print(f" - missing files: {', '.join(plan['missing_files'])}")
        for a in actions:
            print(f" - {a}")

    return 0 if plan["status"] in {"ok", "warn"} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
