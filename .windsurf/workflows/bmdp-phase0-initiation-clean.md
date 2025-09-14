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

### 5. Fix any quality issues

```bash
python tools/processors/workflow_output_fixer.py --business $1
```

## Deliverables

Phase 0 templates will generate:
- `00_sponsor_brief.md` - Sponsor context and commitment
- `01_project_charter.md` - Objectives, scope, success criteria  
- `02_resource_plan.md` - Team, budget, timeline
- `03_readiness_assessment.md` - Risks, stakeholders, go/no-go
- `04_team_roster.csv` - Team member details
- `05_access_matrix.csv` - Access permissions
- `06_sprint_plan.md` - Sprint planning

## Success Criteria

- All templates rendered with business context
- No unsubstituted variables or TBD placeholders
- Quality validation passes
