---
description: Phase 0 - Establishes project foundation with sponsor commitment and initial scope
---

# Phase 0: Initiation

## Steps

### 1. Create initiation directory

```bash
mkdir -p businesses/$1/00_initiation
```

### 2. Render all Phase 0 templates

```bash
python tools/generators/adaptive_template_renderer.py --business $1 --phase 0
```

### 3. Create business manifest

```bash
echo '{"business":"'$1'","phase":0,"status":"in_progress","created":"'$(date +%Y-%m-%d)'"}' > businesses/$1/manifest.json
```

### 4. Run quality validation

```bash
python tools/validators/workflow_quality_assurance.py --business $1
```
