#!/usr/bin/env python3
"""
Template Aligner
Scans Jinja2 templates under templates/deliverables/ and ensures each has
YAML frontmatter aligned with methodologies and workspace rules.

- Dry-run by default: prints planned changes
- Use --apply to write changes in-place (idempotent)

Frontmatter injected when missing:
---
phase: 10_mobilize | 20_understand | 30_design | 00_initiation
artifact: <filename without extension>
methodology_tags: [VPD|BMG|TBI|FINANCIAL]
rule_targets:
  - structure-validation
  - vpd-compliance (if VPD)
  - financial-validation (if FINANCIAL)
  - auto-generation
---
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
import re
import json

TEMPLATES_DIR = Path('templates/deliverables')

PHASE_PREFIX_MAP = {
    '00_': '00_initiation',
    '10_': '10_mobilize',
    '20_': '20_understand',
    '30_': '30_design',
}

# Simple heuristics from filename to methodology tags
KEYWORD_TAGS = [
    ('value_proposition_canvas', ['VPD']),
    ('customer_jobs', ['VPD']),
    ('jobs_to_be_done', ['VPD']),
    ('pain_gain', ['VPD']),
    ('canvas_v0', ['BMG']),
    ('prototype', ['BMG']),
    ('selection_criteria', ['BMG']),
    ('financials_cashflow', ['FINANCIAL']),
    ('financial_projections', ['FINANCIAL', 'BMG']),
    ('test_cards', ['TBI']),
    ('concept_cards', ['TBI']),
    ('assumption_backlog', ['TBI']),
    ('interviews', ['VPD']),
    ('screener', ['VPD']),
    ('insights', ['VPD', 'BMG']),
]

DEFAULT_RULES = ['structure-validation', 'auto-generation']

FRONTMATTER_RE = re.compile(r"^---\s*\n[\s\S]*?\n---\s*\n", re.MULTILINE)


def infer_phase(filename: str, relpath: Path) -> str:
    # From directory if under 32_prototypes
    if '32_prototypes' in str(relpath.parent):
        return '30_design'
    for prefix, phase in PHASE_PREFIX_MAP.items():
        if filename.startswith(prefix):
            return phase
    # Fallback by directory
    parts = relpath.parts
    for p in parts:
        if p.startswith(tuple(PHASE_PREFIX_MAP.keys())):
            return PHASE_PREFIX_MAP[p[:3]]
    return '00_initiation'


def infer_tags(stem: str) -> list[str]:
    tags: set[str] = set()
    s = stem.lower()
    for key, taglist in KEYWORD_TAGS:
        if key in s:
            tags.update(taglist)
    return sorted(tags) if tags else []


def build_frontmatter(phase: str, artifact: str, tags: list[str]) -> str:
    rules = list(DEFAULT_RULES)
    if 'VPD' in tags:
        rules.append('vpd-compliance')
    if 'FINANCIAL' in tags:
        rules.append('financial-validation')
    fm = {
        'phase': phase,
        'artifact': artifact,
        'methodology_tags': tags,
        'rule_targets': rules,
    }
    # Minimal YAML emitter (no external deps)
    def yaml_list(key, items):
        lines = [f"{key}:"]
        for it in items:
            lines.append(f"  - {it}")
        return '\n'.join(lines)

    lines = ["---", f"phase: {fm['phase']}", f"artifact: {fm['artifact']}"]
    if fm['methodology_tags']:
        lines.append(yaml_list('methodology_tags', fm['methodology_tags']))
    lines.append(yaml_list('rule_targets', fm['rule_targets']))
    lines.append("---\n")
    return '\n'.join(lines)


def process_file(path: Path, apply: bool) -> dict:
    text = path.read_text(encoding='utf-8')
    has_frontmatter = FRONTMATTER_RE.match(text) is not None
    filename = path.name
    stem = filename.replace('.j2', '')
    phase = infer_phase(filename, path.relative_to(TEMPLATES_DIR))
    artifact = stem
    tags = infer_tags(stem)
    inserted = False

    if not has_frontmatter:
        fm = build_frontmatter(phase, artifact, tags)
        new_text = fm + text
        if apply:
            path.write_text(new_text, encoding='utf-8')
        inserted = True
    else:
        new_text = text

    return {
        'file': str(path),
        'had_frontmatter': has_frontmatter,
        'inserted_frontmatter': inserted,
        'phase': phase,
        'artifact': artifact,
        'tags': tags,
    }


def scan_templates(apply: bool, limit: int | None = None) -> list[dict]:
    results = []
    count = 0
    for p in sorted(TEMPLATES_DIR.rglob('*.j2')):
        # Only markdown-like and csv templates benefit from frontmatter
        if not (p.suffix == '.j2' and (p.name.endswith('.md.j2') or p.name.endswith('.csv.j2') or p.name.endswith('.json.j2'))):
            continue
        res = process_file(p, apply)
        results.append(res)
        count += 1
        if limit and count >= limit:
            break
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description='Align templates with methodology and workspace rule frontmatter')
    parser.add_argument('--apply', action='store_true', help='Write changes to files (default: dry-run)')
    parser.add_argument('--limit', type=int, help='Process only first N templates')
    args = parser.parse_args(argv)

    if not TEMPLATES_DIR.exists():
        print(f"ERROR: Templates dir not found: {TEMPLATES_DIR}")
        return 1

    results = scan_templates(apply=args.apply, limit=args.limit)
    inserted = sum(1 for r in results if r['inserted_frontmatter'])
    print(f"Templates scanned: {len(results)}")
    print(f"Frontmatter inserted: {inserted}")

    # Print a compact JSON summary for downstream use
    print(json.dumps(results[:10], indent=2))
    if not args.apply:
        print("(dry-run) No files modified. Run with --apply to write changes.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
