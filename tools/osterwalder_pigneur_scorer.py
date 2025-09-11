#!/usr/bin/env python3
"""
Osterwalder & Pigneur Scorer
Computes methodology compliance scores across VPD, BMG, and TBI layers.

Usage:
  python tools/osterwalder_pigneur_scorer.py --business businesses/grower [--format json]

Notes:
- Placeholder scoring combining simple heuristics until detailed analysis is added.
- Weighting inspired by QA workflow: VPD 35%, BMG 40%, TBI 25%.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

# Default weights
VPD_W = 0.35
BMG_W = 0.40
TBI_W = 0.25


def simple_presence_score(path: Path, files: list[tuple[str, str]]) -> float:
    if not files:
        return 0.0
    present = 0
    for d, f in files:
        if (path / d / f).exists():
            present += 1
    return present / len(files)


def compute_scores(business_path: Path) -> dict:
    # Heuristic presence-based scoring as placeholder
    vpd_files = [
        ("10_mobilize", "value_proposition_canvas.md"),
        ("10_mobilize", "customer_jobs_analysis.md"),
        ("20_understand", "pain_gain_mapping.md"),
    ]
    bmg_files = [
        ("10_mobilize", "business_model_canvas.md"),
        ("30_design", "viability_assessment.md"),
    ]
    tbi_files = [
        ("20_understand", "assumption_testing.md"),
        ("20_understand", "evidence_ledger.csv"),
        ("30_design", "prototype_testing.md"),
    ]

    vpd = simple_presence_score(business_path, vpd_files)
    bmg = simple_presence_score(business_path, bmg_files)
    tbi = simple_presence_score(business_path, tbi_files)
    overall = VPD_W * vpd + BMG_W * bmg + TBI_W * tbi

    return {
        "business": business_path.name,
        "scores": {"vpd": vpd, "bmg": bmg, "tbi": tbi, "overall": overall},
        "weights": {"vpd": VPD_W, "bmg": BMG_W, "tbi": TBI_W},
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="O&P methodology compliance scorer")
    parser.add_argument("--business", required=True, help="Path to business root")
    parser.add_argument("--format", choices=["json", "summary"], default="summary")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    business_path = Path(args.business).resolve()
    if not business_path.exists():
        print(f"Error: business path not found: {business_path}", file=sys.stderr)
        return 2

    result = compute_scores(business_path)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        s = result["scores"]
        print(f"[O&P] business={result['business']} vpd={s['vpd']:.2f} bmg={s['bmg']:.2f} tbi={s['tbi']:.2f} overall={s['overall']:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
