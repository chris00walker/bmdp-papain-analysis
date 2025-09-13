#!/usr/bin/env python3
"""
Prototype: Hybrid Parser-LLM Pipeline
Combines enhanced parser with LLM-powered variable expansion
"""

import sys
import os
sys.path.append('/home/chris/bmdp')

from tools.parsers.brief_parser import export_environment_variables, BusinessBriefParser
from typing import Dict, Set, Any
import re

class HybridParserLLM:
    """Hybrid approach: Enhanced parser + LLM variable expansion"""
    
    def __init__(self):
        self.parser = BusinessBriefParser()
        
    def generate_variables(self, business_data: Dict, required_vars: Set[str]) -> Dict[str, str]:
        """Generate variables using hybrid parser-LLM approach"""
        
        # Step 1: Get core variables from enhanced parser
        mock_business_data = {
            'sections': {
                'title': f"{business_data.get('business_type', 'Business')} Operations",
                'value_proposition': ['Deliver high-quality products and services'],
                'customer_segments': ['Primary target customers'],
                'key_activities': ['Core business operations'],
                'key_resources': ['Essential business resources'],
                'revenue_streams': ['Primary revenue generation'],
                'critical_risks': ['Market volatility', 'Operational challenges', 'Regulatory changes']
            },
            'frontmatter': {
                'capital_bounds_bbd': {
                    'min': business_data.get('capital_min', 750000),
                    'max': business_data.get('capital_max', 2500000)
                },
                'financial_method': {
                    'horizon_years': 5,
                    'discount_rate_pct': 15
                },
                'project_execution': {
                    'team_size': 5,
                    'timeline_weeks': 52
                }
            }
        }
        
        # Generate core variables using enhanced parser
        env_output = export_environment_variables(mock_business_data, business_data.get('business_slug', 'business'))
        core_vars = self._parse_env_output(env_output)
        
        # Step 2: Use LLM-like logic to fill remaining variables
        missing_vars = required_vars - set(core_vars.keys())
        llm_vars = self._generate_llm_variables(missing_vars, business_data, core_vars)
        
        # Combine results
        all_vars = {**core_vars, **llm_vars}
        return all_vars
    
    def _parse_env_output(self, env_output: str) -> Dict[str, str]:
        """Parse environment variable output into dictionary"""
        vars_dict = {}
        for line in env_output.split('\n'):
            if line.startswith('export '):
                match = re.match(r'export ([^=]+)="([^"]*)"', line)
                if match:
                    vars_dict[match.group(1)] = match.group(2)
        return vars_dict
    
    def _generate_llm_variables(self, missing_vars: Set[str], business_data: Dict, 
                               core_vars: Dict[str, str]) -> Dict[str, str]:
        """Simulate LLM variable generation using business context"""
        llm_vars = {}
        
        business_type = business_data.get('business_type', 'Business').lower()
        industry = business_data.get('industry_context', 'General').lower()
        
        for var in missing_vars:
            var_lower = var.lower()
            
            # Market and financial variables
            if 'market_size' in var_lower:
                if 'agriculture' in industry:
                    llm_vars[var] = "$2.5B regional agricultural market"
                else:
                    llm_vars[var] = "$1.2B addressable market"
                    
            elif 'competitive_position' in var_lower:
                llm_vars[var] = "Differentiated local player with quality focus"
                
            elif 'acquisition_cost' in var_lower:
                llm_vars[var] = "$150 per customer"
                
            elif 'y1_revenue' in var_lower:
                capital = int(core_vars.get('CAPITAL_MIN', '750000'))
                projected_revenue = int(capital * 0.3)  # 30% of capital as Y1 revenue
                llm_vars[var] = f"${projected_revenue:,}"
                
            # Technology and operational variables
            elif 'tech_requirements' in var_lower:
                if 'agriculture' in industry:
                    llm_vars[var] = "Basic processing equipment, quality control systems"
                else:
                    llm_vars[var] = "Standard business technology stack"
                    
            elif 'regulatory_requirements' in var_lower:
                if 'agriculture' in industry:
                    llm_vars[var] = "Organic certification, food safety compliance"
                else:
                    llm_vars[var] = "Standard business licensing and compliance"
                    
            elif 'partnership_strategy' in var_lower:
                llm_vars[var] = "Strategic partnerships with key suppliers and distributors"
                
            elif 'gtm_timeline' in var_lower:
                timeline_weeks = core_vars.get('TOTAL_TIMELINE_WEEKS', '52')
                gtm_weeks = int(int(timeline_weeks) * 0.6)  # 60% of total timeline
                llm_vars[var] = f"{gtm_weeks} weeks from project start"
                
            elif 'funding_requirements' in var_lower:
                budget = core_vars.get('TOTAL_BMDP_BUDGET', '100000')
                additional_funding = int(int(budget) * 3)  # 3x BMDP budget for operations
                llm_vars[var] = f"${additional_funding:,} operational funding"
                
            elif 'exit_strategy' in var_lower:
                llm_vars[var] = "Strategic acquisition or management buyout after 5-7 years"
                
            # Default fallback
            else:
                llm_vars[var] = f"Context-appropriate {var.lower().replace('_', ' ')} for {business_type} business"
        
        return llm_vars
