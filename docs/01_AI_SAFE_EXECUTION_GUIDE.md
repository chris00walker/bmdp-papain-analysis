---
description: AI-Safe Workflow Execution Guide - Ensures automated compliance during AI workflow execution
---

# AI-Safe Workflow Execution Guide

## Problem Statement

AI workflow execution fails despite clear instructions due to:

- Parameter substitution inconsistency
- Creative interpretation over strict compliance  
- Context loss across execution sessions
- No validation feedback loops
- Template vs execution confusion
- Incorrect working directory assumptions

## 3-Layer Automated Compliance Solution

### Layer 1: Pre-Execution Validation

**Purpose**: Ensure readiness before AI begins workflow execution

```bash
# Before executing any phase workflow (run from project root)
python tools/workflow_checkpoint.py --business {business_slug} execute --phase {phase} --workflow {workflow_file}
```

**What it does**:

- Validates previous phase completion
- Records execution start checkpoint
- Provides AI with explicit parameter substitution instructions
- Sets compliance expectations

### Layer 2: Real-Time Enforcement

**Purpose**: Automated compliance checking and fixing during execution

```bash
# Run after AI completes each major deliverable section (run from project root)
python tools/workflow_enforcer.py --business {business_slug}
```

**What it does**:

- Detects missing deliverables immediately
- Auto-generates template content for missing files
- Fixes file naming violations
- Provides immediate feedback to AI

### Layer 3: Post-Execution Validation

**Purpose**: Comprehensive validation before phase completion

```bash
# After AI completes entire phase (run from project root)
python tools/workflow_checkpoint.py --business {business_slug} post-validate --phase {phase}
```

**What it does**:

- Validates 100% deliverable completion
- Records phase completion checkpoint
- Blocks progression until compliance achieved
- Generates compliance report

## AI Execution Protocol

### For AI Agents Executing Workflows

1. **ALWAYS run pre-execution validation first**

   ```bash
   # Run from project root directory
   python tools/workflow_checkpoint.py --business {business_slug} execute --phase {phase} --workflow {workflow_file}
   ```

2. **Follow parameter substitution exactly**:
   - Replace `{business_slug}` with actual business name
   - Replace `$1` with business parameter
   - Use exact file names from workflow requirements

3. **Run enforcement check after each section**:

   ```bash
   # Run from project root directory
   python tools/workflow_enforcer.py --business {business_slug}
   ```

4. **MANDATORY post-execution validation**:

   ```bash
   # Run from project root directory
   python tools/workflow_checkpoint.py --business {business_slug} post-validate --phase {phase}
   ```

5. **Do NOT proceed to next phase until validation passes**

## Validation Tools

**Note**: All tools are located in the `tools/` directory and should be run from the project root.

### workflow_validator.py

- Comprehensive compliance checking
- Identifies missing/extra/misnamed files
- Generates compliance scores
- JSON and summary output formats

### workflow_enforcer.py  

- Automated fix generation
- Template content creation
- File naming corrections
- Immediate compliance restoration

### workflow_checkpoint.py

- Phase progression control
- Execution state tracking
- Validation gate enforcement
- Status reporting

## Usage Examples

### Check current compliance

```bash
# Run from project root directory
python tools/workflow_validator.py --business grower --format summary
```

### Fix all compliance issues

```bash
# Run from project root directory
python tools/workflow_enforcer.py --business processor
```

### Execute phase with validation

```bash
# Run from project root directory
python tools/workflow_checkpoint.py --business distributor execute --phase 00_initiation --workflow bmdp-phase0-initiation.md
```

### Get workflow status

```bash
# Run from project root directory
python tools/workflow_checkpoint.py --business marketplace status
```

## Critical Success Factors

1. **Mandatory Validation**: Never skip pre/post execution validation
2. **Correct Working Directory**: Always run tools from project root (`/home/chris/bmdp`)
3. **Exact Naming**: Use workflow-specified file names exactly
4. **Complete Deliverables**: All required files must be created
5. **Parameter Consistency**: Apply substitution uniformly
6. **Context Preservation**: Use checkpoints to maintain state

## Failure Prevention

### Common AI Failure Modes → Solutions

| Failure Mode | Solution |
|--------------|----------|
| Parameter substitution errors | Pre-execution validation with explicit instructions |
| Creative file naming | Real-time enforcement with naming validation |
| Missing deliverables | Auto-generation of missing files with templates |
| Context loss | Checkpoint system preserves execution state |
| Incomplete phases | Post-validation blocks progression until 100% complete |

## Integration with Existing Workflows

### Modified Workflow Execution Pattern

```bash
# 1. Pre-execution validation (run from project root)
python tools/workflow_checkpoint.py --business {business} execute --phase {phase} --workflow {workflow_file}

# 2. Execute original workflow with parameter substitution
# [Original workflow commands with {business_slug} replaced]

# 3. Real-time enforcement (run periodically during execution)
python tools/workflow_enforcer.py --business {business}

# 4. Post-execution validation (mandatory before completion)
python tools/workflow_checkpoint.py --business {business} post-validate --phase {phase}
```

## Success Metrics

- **100% Deliverable Completion**: All required files created with correct names
- **Zero Naming Violations**: Exact adherence to workflow specifications  
- **Consistent Parameter Substitution**: Uniform application across all files
- **Phase Gate Compliance**: No progression without validation
- **Context Preservation**: Execution state maintained across sessions

This system transforms unreliable AI workflow execution into a deterministic, compliant process with automated validation and enforcement.
