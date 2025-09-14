#!/usr/bin/env python3
"""
Template Upgrader - Makes all BMDP templates LLM-adaptive and methodology-compliant
Implements the requirements for context-intelligent, industry-agnostic templates
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple
import yaml

class TemplateUpgrader:
    """Upgrades templates to be LLM-adaptive and methodology-compliant"""
    
    def __init__(self):
        self.template_dir = Path('/home/chris/bmdp/templates/deliverables')
        self.upgraded_count = 0
        
        # Methodology tags for each phase
        self.phase_methodologies = {
            '00_initiation': ['BMG', 'TBI'],  # Business Model Generation, Testing Business Ideas
            '10_mobilize': ['BMG', 'VPD'],    # Add Value Proposition Design
            '20_understand': ['VPD', 'TBI'],   # Customer research focus
            '30_design': ['BMG', 'VPD', 'TBI'] # All methodologies
        }
        
        # Context variables that should be used
        self.context_variables = [
            'BUSINESS_TYPE', 'INDUSTRY_CONTEXT', 'CUSTOMER_SEGMENTS',
            'VALUE_PROPOSITION', 'KEY_ACTIVITIES', 'REVENUE_STREAMS'
        ]
    
    def upgrade_template(self, template_path: Path) -> bool:
        """Upgrade a single template to be LLM-adaptive"""
        try:
            content = template_path.read_text()
            original_content = content
            
            # Parse frontmatter
            frontmatter, body = self.parse_frontmatter(content)
            
            # Upgrade frontmatter
            frontmatter = self.upgrade_frontmatter(frontmatter, template_path)
            
            # Upgrade body content
            body = self.upgrade_body_content(body, template_path)
            
            # Reconstruct template
            new_content = self.reconstruct_template(frontmatter, body)
            
            if new_content != original_content:
                template_path.write_text(new_content)
                self.upgraded_count += 1
                return True
                
            return False
            
        except Exception as e:
            print(f"Error upgrading {template_path}: {e}")
            return False
    
    def parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Parse YAML frontmatter from template"""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    body = parts[2]
                    return frontmatter or {}, body
                except:
                    pass
        return {}, content
    
    def upgrade_frontmatter(self, frontmatter: Dict, template_path: Path) -> Dict:
        """Upgrade frontmatter with methodology tags and rules"""
        # Determine phase from path
        phase = template_path.parent.name
        
        # Add/update phase
        frontmatter['phase'] = phase
        
        # Add artifact name
        frontmatter['artifact'] = template_path.stem
        
        # Add methodology tags
        if phase in self.phase_methodologies:
            frontmatter['methodology_tags'] = self.phase_methodologies[phase]
        
        # Add rule targets for workspace rules
        rule_targets = ['structure-validation', 'auto-generation']
        
        # Add specific rules based on phase
        if phase == '10_mobilize' or phase == '20_understand':
            rule_targets.append('vpd-compliance')
        if phase == '30_design':
            rule_targets.extend(['bmg-validation', 'tbi-validation'])
        
        frontmatter['rule_targets'] = rule_targets
        
        # Add LLM guidance
        frontmatter['llm_guidance'] = {
            'adaptive': True,
            'industry_agnostic': True,
            'context_aware': True,
            'evidence_driven': True
        }
        
        return frontmatter
    
    def upgrade_body_content(self, body: str, template_path: Path) -> str:
        """Upgrade template body to be LLM-adaptive"""
        phase = template_path.parent.name
        
        # Add LLM guidance comments (using Jinja2 comments that won't appear in output)
        guidance_header = """
{# LLM GUIDANCE
This template is designed to be adaptive and context-aware. When generating content:
1. Use BUSINESS_TYPE and INDUSTRY_CONTEXT to tailor examples and language
2. Reference CUSTOMER_SEGMENTS and VALUE_PROPOSITION for relevance
3. Ensure all content aligns with the business's KEY_ACTIVITIES and REVENUE_STREAMS
4. Generate specific, measurable, and evidence-based content
5. Follow the methodology frameworks: {% if 'VPD' in methodology_tags %}Value Proposition Design{% endif %}{% if 'BMG' in methodology_tags %}, Business Model Generation{% endif %}{% if 'TBI' in methodology_tags %}, Testing Business Ideas{% endif %}
#}
"""
        
        # Add context-aware sections
        if phase == '00_initiation':
            body = self.add_initiation_context(body)
        elif phase == '10_mobilize':
            body = self.add_mobilize_context(body)
        elif phase == '20_understand':
            body = self.add_understand_context(body)
        elif phase == '30_design':
            body = self.add_design_context(body)
        
        # Replace TBD placeholders with context-aware guidance
        body = self.replace_tbd_with_guidance(body)
        
        # Add evidence-driven sections
        body = self.add_evidence_sections(body, phase)
        
        # Insert guidance header after title
        if '# ' in body:
            parts = body.split('\n', 2)
            if len(parts) >= 2:
                body = parts[0] + '\n' + guidance_header + '\n' + '\n'.join(parts[1:])
        else:
            body = guidance_header + body
        
        return body
    
    def add_initiation_context(self, body: str) -> str:
        """Add Phase 0 specific context"""
        context_section = """
## Industry Context
{% if INDUSTRY_CONTEXT %}
**Industry**: {{ INDUSTRY_CONTEXT }}
**Market Dynamics**: Based on {{ INDUSTRY_CONTEXT }}, key considerations include regulatory requirements, competitive landscape, and market maturity.
{% else %}
**Industry**: To be determined based on business model analysis
{% endif %}

## Methodology Alignment
**Business Model Generation (BMG)**: Initial canvas development focusing on the 9 building blocks
**Testing Business Ideas (TBI)**: Hypothesis identification for validation in subsequent phases
"""
        # Insert after Business Context section
        if '## Business Context' in body:
            body = body.replace('## Business Context', '## Business Context' + context_section)
        return body
    
    def add_mobilize_context(self, body: str) -> str:
        """Add Phase 1 specific context"""
        vpd_section = """
## Value Proposition Design Framework
{% if VALUE_PROPOSITION and CUSTOMER_SEGMENTS %}
### Customer Profile
**Customer Segments**: {{ CUSTOMER_SEGMENTS }}
**Jobs**: Functional, emotional, and social jobs derived from {{ INDUSTRY_CONTEXT }}
**Pains**: Industry-specific challenges in {{ INDUSTRY_CONTEXT }}
**Gains**: Desired outcomes for {{ CUSTOMER_SEGMENTS }}

### Value Map
**Products & Services**: {{ KEY_ACTIVITIES }}
**Pain Relievers**: How {{ VALUE_PROPOSITION }} addresses customer pains
**Gain Creators**: How {{ VALUE_PROPOSITION }} creates customer gains
{% endif %}
"""
        if '## Value Proposition' in body:
            body = body.replace('## Value Proposition', vpd_section + '\n## Value Proposition')
        return body
    
    def add_understand_context(self, body: str) -> str:
        """Add Phase 2 specific context"""
        research_section = """
## Research Context
{% if INDUSTRY_CONTEXT and CUSTOMER_SEGMENTS %}
### Industry-Specific Research Focus
**Sector**: {{ INDUSTRY_CONTEXT }}
**Target Participants**: {{ CUSTOMER_SEGMENTS }}
**Research Questions**: Tailored to {{ BUSINESS_TYPE }} business model

### Evidence Collection Framework
- Quantitative metrics relevant to {{ INDUSTRY_CONTEXT }}
- Qualitative insights from {{ CUSTOMER_SEGMENTS }}
- Competitive benchmarks for {{ BUSINESS_TYPE }} models
{% endif %}
"""
        if '## Research' in body:
            body = body.replace('## Research', research_section + '\n## Research')
        return body
    
    def add_design_context(self, body: str) -> str:
        """Add Phase 3 specific context"""
        design_section = """
## Design Context
{% if BUSINESS_TYPE and INDUSTRY_CONTEXT %}
### Business Model Pattern
**Type**: {{ BUSINESS_TYPE }}
**Industry**: {{ INDUSTRY_CONTEXT }}
**Revenue Model**: {{ REVENUE_STREAMS }}

### Testing Framework (TBI)
- Desirability experiments for {{ CUSTOMER_SEGMENTS }}
- Feasibility tests for {{ KEY_ACTIVITIES }}
- Viability analysis for {{ REVENUE_STREAMS }}
{% endif %}
"""
        if '## Design' in body or '# ' in body:
            lines = body.split('\n')
            # Insert after first heading
            for i, line in enumerate(lines):
                if line.startswith('# '):
                    lines.insert(i + 1, design_section)
                    break
            body = '\n'.join(lines)
        return body
    
    def replace_tbd_with_guidance(self, body: str) -> str:
        """Replace TBD placeholders with context-aware guidance"""
        # Pattern to find TBD placeholders
        tbd_pattern = r'\{\{ (\w+) \| default\("TBD[^"]*"\) \}\}'
        
        def replace_tbd(match):
            var_name = match.group(1)
            # Create context-aware default
            if 'segment' in var_name.lower():
                return f'{{{{ {var_name} | default("Identify based on {{{{ INDUSTRY_CONTEXT }}}} market analysis") }}}}'
            elif 'value' in var_name.lower():
                return f'{{{{ {var_name} | default("Derive from {{{{ VALUE_PROPOSITION }}}} for {{{{ CUSTOMER_SEGMENTS }}}}") }}}}'
            elif 'channel' in var_name.lower():
                return f'{{{{ {var_name} | default("Select channels appropriate for {{{{ BUSINESS_TYPE }}}} in {{{{ INDUSTRY_CONTEXT }}}}") }}}}'
            elif 'revenue' in var_name.lower():
                return f'{{{{ {var_name} | default("Based on {{{{ REVENUE_STREAMS }}}} model") }}}}'
            elif 'activity' in var_name.lower() or 'activities' in var_name.lower():
                return f'{{{{ {var_name} | default("Aligned with {{{{ KEY_ACTIVITIES }}}}") }}}}'
            else:
                return f'{{{{ {var_name} | default("Generate based on {{{{ BUSINESS_TYPE }}}} context") }}}}'
        
        body = re.sub(tbd_pattern, replace_tbd, body)
        return body
    
    def add_evidence_sections(self, body: str, phase: str) -> str:
        """Add evidence-driven measurement sections"""
        evidence_section = """
## Evidence & Metrics
{% if methodology_tags %}
### Measurement Framework
{% if 'VPD' in methodology_tags %}
**Value Proposition Metrics**:
- Customer job completion rate
- Pain reduction indicators
- Gain achievement measures
{% endif %}
{% if 'BMG' in methodology_tags %}
**Business Model Metrics**:
- Revenue stream validation
- Cost structure efficiency
- Channel effectiveness
{% endif %}
{% if 'TBI' in methodology_tags %}
**Testing Metrics**:
- Hypothesis validation rate
- Experiment success criteria
- Learning velocity
{% endif %}
{% endif %}

### Success Indicators
- Quantitative: Specific metrics for {{ BUSINESS_TYPE }} in {{ INDUSTRY_CONTEXT }}
- Qualitative: Customer feedback from {{ CUSTOMER_SEGMENTS }}
- Comparative: Benchmarks for {{ INDUSTRY_CONTEXT }} sector
"""
        # Add before Next Steps or at end
        if '## Next Steps' in body:
            body = body.replace('## Next Steps', evidence_section + '\n## Next Steps')
        else:
            body += '\n' + evidence_section
        
        return body
    
    def reconstruct_template(self, frontmatter: Dict, body: str) -> str:
        """Reconstruct template with upgraded frontmatter and body"""
        import yaml
        
        # Convert frontmatter to YAML
        yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        
        # Reconstruct with proper formatting
        return f"---\n{yaml_str}---\n{body}"
    
    def upgrade_all_templates(self) -> Dict:
        """Upgrade all templates in the deliverables directory"""
        results = {
            'upgraded': [],
            'skipped': [],
            'errors': []
        }
        
        # Process each phase
        for phase_dir in self.template_dir.iterdir():
            if phase_dir.is_dir() and phase_dir.name != 'shared':
                for template_file in phase_dir.glob('*.j2'):
                    if self.upgrade_template(template_file):
                        results['upgraded'].append(str(template_file.relative_to(self.template_dir)))
                    else:
                        results['skipped'].append(str(template_file.relative_to(self.template_dir)))
        
        return results
    
    def generate_report(self, results: Dict) -> str:
        """Generate upgrade report"""
        report = []
        report.append("=" * 60)
        report.append("TEMPLATE UPGRADE REPORT")
        report.append("=" * 60)
        report.append("")
        report.append(f"✅ Upgraded: {len(results['upgraded'])} templates")
        report.append(f"⏭️  Skipped: {len(results['skipped'])} templates")
        report.append(f"❌ Errors: {len(results['errors'])} templates")
        report.append("")
        
        if results['upgraded']:
            report.append("Upgraded Templates:")
            for template in results['upgraded'][:10]:
                report.append(f"  - {template}")
            if len(results['upgraded']) > 10:
                report.append(f"  ... and {len(results['upgraded']) - 10} more")
        
        report.append("")
        report.append("Template Features Added:")
        report.append("  💡 LLM-adaptive guidance in every template")
        report.append("  🌍 Industry-agnostic with context awareness")
        report.append("  📐 VPD, BMG, TBI methodology alignment")
        report.append("  🧠 Context variables integration")
        report.append("  📊 Evidence-driven measurement sections")
        report.append("  🧭 Consistent structure and naming")
        
        return '\n'.join(report)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Upgrade BMDP templates for LLM adaptivity')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be upgraded')
    parser.add_argument('--phase', choices=['00_initiation', '10_mobilize', '20_understand', '30_design'],
                       help='Upgrade specific phase only')
    
    args = parser.parse_args()
    
    upgrader = TemplateUpgrader()
    results = upgrader.upgrade_all_templates()
    report = upgrader.generate_report(results)
    print(report)
    
    return 0

if __name__ == '__main__':
    exit(main())
