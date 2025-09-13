#!/usr/bin/env python3
"""
VPD Canvas Creator
Creates scaffold files for Value Proposition Canvas and related VPD deliverables.

Usage:
  python tools/vpd_canvas_creator.py --business businesses/grower [--apply]

Notes:
- Safe by default: dry-run (no modifications). Use --apply to create files.
- Idempotent: will not overwrite existing files.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

VPD_FILES = [
    ("10_mobilize", "value_proposition_canvas.md"),
    ("10_mobilize", "customer_jobs_analysis.md"),
    ("20_understand", "pain_gain_mapping.md"),
]

VPD_TEMPLATES = {
    "value_proposition_canvas.md": "# Value Proposition Canvas\n\n## Customer Profile\n- Jobs (functional, emotional, social)\n- Pains\n- Gains\n\n## Value Map\n- Products & Services\n- Pain Relievers\n- Gain Creators\n",
    "customer_jobs_analysis.md": "# Customer Jobs Analysis\n\n- Functional Jobs\n- Emotional Jobs\n- Social Jobs\n",
    "pain_gain_mapping.md": "# Pain & Gain Mapping\n\n- Pains (severity/importance)\n- Gains (relevance/impact)\n",
}


def plan_creation(business_path: Path) -> dict:
    missing = []
    for d, f in VPD_FILES:
        target = business_path / d / f
        if not target.exists():
            missing.append(str(target))
    return {"business": business_path.name, "to_create": missing}


def apply_creation(plan: dict) -> list[str]:
    actions: list[str] = []
    for full in plan.get("to_create", []):
        p = Path(full)
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            content = VPD_TEMPLATES.get(p.name, "# TODO\n")
            p.write_text(content, encoding="utf-8")
            actions.append(f"created: {p}")
    return actions


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create Value Proposition Design scaffold files")
    parser.add_argument("--business", required=True, help="Path to business root")
    parser.add_argument("--apply", action="store_true", help="Create missing files (idempotent)")
    parser.add_argument("--format", choices=["json", "summary"], default="summary")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    business_path = Path(args.business).resolve()
    if not business_path.exists():
        print(f"Error: business path not found: {business_path}", file=sys.stderr)
        return 2

    plan = plan_creation(business_path)
    actions: list[str] = []
    if args.apply:
        actions = apply_creation(plan)

    if args.format == "json":
        print(json.dumps({"plan": plan, "actions": actions}, indent=2))
    else:
        print(f"[VPD] business={plan['business']}")
        if plan["to_create"]:
            print(" - missing files:")
            for f in plan["to_create"]:
                print(f"   - {f}")
        for a in actions:
            print(f" - {a}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
