#!/usr/bin/env python3
"""
Adaptive Template Renderer - Renders LLM-adaptive templates with full context
Implements the template rendering for upgraded methodology-compliant templates
"""

import sys
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, meta
import yaml
import subprocess
import json

sys.path.append('/home/chris/bmdp')

class AdaptiveTemplateRenderer:
    """Renders upgraded templates with LLM-adaptive content"""
    
    def __init__(self, business: str):
        self.business = business
        self.template_base = Path('/home/chris/bmdp/templates/deliverables')
        
        # Get business context variables
        self.context = self._get_business_context()
        
        # Add methodology context
        self.context['methodology_tags'] = ['VPD', 'BMG', 'TBI']
        
    def _get_business_context(self) -> dict:
        """Get all context variables for the business"""
        # Get parser variables
        cmd = [
            'python', 'tools/parsers/brief_parser.py',
            '--business', self.business,
            '--output-format', 'env'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd='/home/chris/bmdp')
        
        context = {
            'business_slug': self.business,
            'BUSINESS_TYPE': self.business.title(),
            'INDUSTRY_CONTEXT': self._get_industry_context(),
        }
        
        # Parse environment variables
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('export ') and '=' in line:
                    parts = line.replace('export ', '').split('=', 1)
                    key = parts[0]
                    value = parts[1].strip("'\"")
                    context[key] = value
                    # Also add lowercase version for compatibility
                    context[key.lower()] = value
        
        # Add uppercase versions of key variables
        if 'VALUE_PROPOSITION' not in context and 'value_proposition' in context:
            context['VALUE_PROPOSITION'] = context['value_proposition']
        if 'CUSTOMER_SEGMENTS' not in context and 'customer_segments' in context:
            context['CUSTOMER_SEGMENTS'] = context['customer_segments']
        if 'KEY_ACTIVITIES' not in context and 'key_activities' in context:
            context['KEY_ACTIVITIES'] = context['key_activities']
        if 'REVENUE_STREAMS' not in context and 'revenue_streams' in context:
            context['REVENUE_STREAMS'] = context['revenue_streams']
            
        return context
    
    def _get_industry_context(self) -> str:
        """Determine industry context from business type"""
        contexts = {
            'grower': 'Agriculture and Cultivation',
            'processor': 'Manufacturing and Processing',
            'distributor': 'Logistics and Distribution',
            'marketplace': 'Digital Platform and E-commerce'
        }
        return contexts.get(self.business, 'General Business')
    
    def render_template(self, template_path: str, output_path: str) -> bool:
        """Render a single template with full context"""
        try:
            # Setup Jinja2 environment
            template_file = Path(template_path)
            env = Environment(
                loader=FileSystemLoader(str(template_file.parent)),
                trim_blocks=True,
                lstrip_blocks=True
            )
            
            # Load and render template
            template = env.get_template(template_file.name)
            
            # Add LLM-adaptive defaults for missing variables
            enhanced_context = self._enhance_context_with_llm_defaults(self.context.copy())
            
            # Render with enhanced context
            rendered = template.render(**enhanced_context)
            
            # Write output
            output = Path(output_path)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered)
            
            return True
            
        except Exception as e:
            print(f"Error rendering {template_path}: {e}")
            return False
    
    def _enhance_context_with_llm_defaults(self, context: dict) -> dict:
        """Add LLM-adaptive defaults for missing variables"""
        
        # Business-specific enhancements
        if self.business == 'processor':
            context.setdefault('value_proposition', 
                'Transform raw materials into high-quality processed products with efficiency and reliability')
            context.setdefault('customer_segments', 
                'B2B manufacturers, distributors, and retail chains requiring processed goods')
            context.setdefault('key_activities', 
                'Raw material processing, quality control, packaging, and distribution')
            context.setdefault('revenue_streams', 
                'Product sales, processing fees, and value-added services')
            context.setdefault('key_resources', 
                'Processing facilities, equipment, skilled workforce, and supply chain relationships')
                
        elif self.business == 'grower':
            context.setdefault('value_proposition',
                'Cultivate reliable, traceable crude papain from Barbados')
            context.setdefault('customer_segments',
                'International enzyme processors and regional food processors')
                
        elif self.business == 'distributor':
            context.setdefault('value_proposition',
                'Efficient logistics and distribution network for timely delivery')
            context.setdefault('customer_segments',
                'Retailers, wholesalers, and direct consumers')
                
        elif self.business == 'marketplace':
            context.setdefault('value_proposition',
                'Connect buyers and sellers through a trusted digital platform')
            context.setdefault('customer_segments',
                'Online buyers and sellers seeking convenient transactions')
        
        # Add uppercase versions
        for key in list(context.keys()):
            if key.islower() and key.upper() not in context:
                context[key.upper()] = context[key]
        
        # Add methodology-specific variables
        context['VPD_COMPLIANT'] = True
        context['BMG_COMPLIANT'] = True
        context['TBI_COMPLIANT'] = True
        
        return context
    
    def render_phase(self, phase: str) -> int:
        """Render all templates for a phase"""
        phase_map = {
            '0': '00_initiation',
            '1': '10_mobilize', 
            '2': '20_understand',
            '3': '30_design'
        }
        
        phase_dir = phase_map.get(phase, phase)
        template_dir = self.template_base / phase_dir
        output_dir = Path(f'/home/chris/bmdp/businesses/{self.business}/{phase_dir}')
        
        if not template_dir.exists():
            print(f"Template directory not found: {template_dir}")
            return 0
        
        rendered_count = 0
        for template_file in template_dir.glob('*.j2'):
            # Determine output filename (remove .j2 extension)
            output_file = output_dir / template_file.stem
            
            if self.render_template(str(template_file), str(output_file)):
                rendered_count += 1
                print(f"  ✅ Rendered {template_file.stem}")
            else:
                print(f"  ❌ Failed to render {template_file.stem}")
        
        return rendered_count

def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Render adaptive templates')
    parser.add_argument('--business', required=True,
                       choices=['grower', 'processor', 'distributor', 'marketplace'])
    parser.add_argument('--phase', required=True,
                       choices=['0', '1', '2', '3', 'all'])
    parser.add_argument('--template', help='Specific template to render')
    
    args = parser.parse_args()
    
    renderer = AdaptiveTemplateRenderer(args.business)
    
    if args.template:
        # Render specific template
        template_path = args.template
        output_path = template_path.replace('.j2', '').replace('templates/deliverables', 
                                                               f'businesses/{args.business}')
        if renderer.render_template(template_path, output_path):
            print(f"✅ Rendered {template_path}")
        else:
            print(f"❌ Failed to render {template_path}")
    elif args.phase == 'all':
        # Render all phases
        total = 0
        for phase in ['0', '1', '2', '3']:
            print(f"\nRendering Phase {phase}...")
            count = renderer.render_phase(phase)
            total += count
        print(f"\n✅ Total templates rendered: {total}")
    else:
        # Render specific phase
        print(f"Rendering Phase {args.phase} for {args.business}...")
        count = renderer.render_phase(args.phase)
        print(f"✅ Rendered {count} templates")
    
    return 0

if __name__ == '__main__':
    exit(main())
