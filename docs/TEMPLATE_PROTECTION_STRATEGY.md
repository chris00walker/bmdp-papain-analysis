# Template Protection Strategy

## Problem Statement
Sophisticated BMDP templates containing months of development work were accidentally deleted in commit `7e67047` during modular reorganization. This caused significant regression and required extensive recovery effort.

## Protection Measures

### 1. Git Branch Protection
```bash
# Create protected template branch
git checkout -b template-protection
git push -u origin template-protection

# Protect critical template directories
git config branch.template-protection.mergeoptions "--no-ff"
```

### 2. Pre-commit Hooks
Create `.git/hooks/pre-commit` to prevent template deletion:
```bash
#!/bin/bash
# Check for template file deletions
deleted_templates=$(git diff --cached --name-status | grep "^D.*templates/deliverables.*\.j2$")
if [ ! -z "$deleted_templates" ]; then
    echo "ERROR: Template files are being deleted!"
    echo "$deleted_templates"
    echo "Use 'git commit --allow-template-deletion' to override"
    exit 1
fi
```

### 3. Template Backup Strategy
- **Daily Backups**: Automated backup of templates/ directory
- **Version Tagging**: Tag releases with template versions
- **Recovery Documentation**: Clear recovery procedures

### 4. Safe Refactoring Process
1. **Create Feature Branch**: Never modify templates on main
2. **Template Validation**: Run template tests before merge
3. **Incremental Changes**: Small, reviewable template modifications
4. **Rollback Plan**: Document how to revert each change

### 5. Template Integrity Checks
```bash
# Count template files
find templates/deliverables -name "*.j2" | wc -l

# Verify template structure
python tools/validators/template_validator.py --check-all

# Variable coverage analysis
python tools/analyzers/template_coverage.py
```

### 6. Critical File Monitoring
Monitor these critical paths:
- `templates/deliverables/*/` - All phase templates
- `tools/parsers/parse_business_brief.py` - Hybrid parser
- `templates/template_config.json` - Template configuration

### 7. Recovery Procedures
If templates are lost:
1. **Immediate Assessment**: `git log --oneline --since="1 day ago"`
2. **Recovery Command**: `git checkout <last-good-commit> -- templates/deliverables/`
3. **Variable Standardization**: Run standardization tool
4. **Integration Testing**: Verify parser compatibility

## Implementation Checklist
- [ ] Create template-protection branch
- [ ] Install pre-commit hooks
- [ ] Set up automated backups
- [ ] Document recovery procedures
- [ ] Train team on safe refactoring
- [ ] Implement template validation tests

## Emergency Contacts
- Template Recovery: Use git history before commit 7e67047
- Hybrid Parser Issues: Check parse_business_brief.py integration
- Variable Mismatches: Run standardize_template_variables.py

This strategy prevents future template loss and ensures rapid recovery if issues occur.
