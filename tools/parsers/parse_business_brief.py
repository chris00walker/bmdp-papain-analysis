#!/usr/bin/env python3
"""
Business Brief Parser
Extracts structured data from business brief markdown files
"""

import argparse
import re
import yaml
from pathlib import Path

def parse_brief_file(brief_path):
    """Parse a business brief file and extract structured data"""
    with open(brief_path, 'r') as f:
        content = f.read()
    
    # Split frontmatter and content
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = yaml.safe_load(parts[1])
        markdown_content = parts[2].strip()
    else:
        frontmatter = {}
        markdown_content = content
    
    # Extract sections using regex
    sections = {}
    
    # Extract title
    title_match = re.search(r'^#\s*\*\*(.*?)\*\*', markdown_content, re.MULTILINE)
    sections['title'] = title_match.group(1) if title_match else "Business"
    
    # Extract value proposition
    value_prop_match = re.search(r'\*\*Value Proposition\*\*\n\n(.*?)(?=\n\n\*\*|\Z)', markdown_content, re.DOTALL)
    if value_prop_match:
        sections['value_proposition'] = clean_bullet_points(value_prop_match.group(1))
    
    # Extract customer segments
    customer_match = re.search(r'\*\*Customer Segments\*\*\n\n(.*?)(?=\n\n\*\*|\Z)', markdown_content, re.DOTALL)
    if customer_match:
        sections['customer_segments'] = clean_bullet_points(customer_match.group(1))
    
    # Extract key activities
    activities_match = re.search(r'\*\*Key Activities\*\*\n\n(.*?)(?=\n\n\*\*|\Z)', markdown_content, re.DOTALL)
    if activities_match:
        sections['key_activities'] = clean_bullet_points(activities_match.group(1))
    
    # Extract key resources
    resources_match = re.search(r'\*\*Key Resources\*\*\n\n(.*?)(?=\n\n\*\*|\Z)', markdown_content, re.DOTALL)
    if resources_match:
        sections['key_resources'] = clean_bullet_points(resources_match.group(1))
    
    # Extract channels
    channels_match = re.search(r'\*\*Channels\*\*\n\n(.*?)(?=\n\n\*\*|\Z)', markdown_content, re.DOTALL)
    if channels_match:
        sections['channels'] = clean_bullet_points(channels_match.group(1))
    
    # Extract revenue streams
    revenue_match = re.search(r'\*\*Revenue Streams\*\*\n\n(.*?)(?=\n\n\*\*|\Z)', markdown_content, re.DOTALL)
    if revenue_match:
        sections['revenue_streams'] = clean_bullet_points(revenue_match.group(1))
    
    # Extract cost structure
    cost_match = re.search(r'\*\*Cost Structure\*\*\n\n(.*?)(?=\n\n\*\*|\Z)', markdown_content, re.DOTALL)
    if cost_match:
        sections['cost_structure'] = clean_bullet_points(cost_match.group(1))
    
    # Extract critical risks
    risks_match = re.search(r'\*\*Critical Risks\*\*\n\n(.*?)(?=\n\n\*\*|\Z)', markdown_content, re.DOTALL)
    if risks_match:
        sections['critical_risks'] = clean_bullet_points(risks_match.group(1))
    
    return {
        'frontmatter': frontmatter,
        'sections': sections
    }

def clean_bullet_points(text):
    """Clean and format bullet points from extracted text"""
    lines = text.strip().split('\n')
    cleaned = []
    for line in lines:
        line = line.strip()
        if line and line.startswith('*'):
            # Remove leading * and clean up
            cleaned.append(line[1:].strip())
        elif line and not line.startswith('*') and cleaned:
            # Continuation of previous line
            cleaned[-1] += ' ' + line
    return cleaned

def get_business_number(business_slug):
    """Get business number from slug"""
    mapping = {
        'grower': '1',
        'processor': '2', 
        'distributor': '3',
        'marketplace': '4',
        'b2b-marketplace': '4'
    }
    return mapping.get(business_slug, '1')

def main():
    parser = argparse.ArgumentParser(description='Parse business brief file')
    parser.add_argument('--business', required=True, help='Business slug')
    parser.add_argument('--output-format', choices=['json', 'env'], default='env',
                       help='Output format (default: env)')
    
    args = parser.parse_args()
    
    # Find brief file
    business_number = get_business_number(args.business)
    brief_path = Path(f'brief-{business_number}-{args.business}.md')
    
    if not brief_path.exists():
        print(f"ERROR: Brief file not found: {brief_path}")
        return 1
    
    # Parse brief
    data = parse_brief_file(brief_path)
    
    if args.output_format == 'env':
        # Output as environment variables for shell scripts
        sections = data['sections']
        frontmatter = data['frontmatter']
        print(f"BUSINESS_TITLE='{sections['title']}'")
        print(f"BUSINESS_NUMBER='{get_business_number(args.business)}'")
        print(f"BRIEF_FILE='{brief_path.name}'")
        print(f"CAPITAL_MIN='{frontmatter.get('capital_bounds_bbd', {}).get('min', 0)}'")
        print(f"CAPITAL_MAX='{frontmatter.get('capital_bounds_bbd', {}).get('max', 0)}'")
        print(f"HORIZON_YEARS='{frontmatter.get('financial_method', {}).get('horizon_years', 5)}'")
        print(f"DISCOUNT_RATE='{frontmatter.get('financial_method', {}).get('discount_rate_pct', 15)}'")
        print(f"ROI_TARGET='{frontmatter.get('financial_method', {}).get('roi_target_pct', 20)}'")
        
        # Extract financial metrics
        metrics = frontmatter.get('financial_method', {}).get('metrics', ['IRR', 'NPV', 'ROI'])
        print(f"FINANCIAL_METRICS='{', '.join(metrics)}'")
        
        # Extract project execution parameters
        project_exec = frontmatter.get('project_execution', {})
        team_size = project_exec.get('team_size', 4)
        
        # Calculate dynamic phase durations from percentages
        timeline_weeks = project_exec.get('timeline_weeks', 52)
        phase_ratios = project_exec.get('phase_ratios', {})
        
        # Use percentage-based calculations or fall back to fixed values
        if phase_ratios:
            discovery_pct = phase_ratios.get('discovery_pct', 50)
            validation_pct = phase_ratios.get('validation_pct', 33)
            scaling_pct = phase_ratios.get('scaling_pct', 17)
            
            phase1_weeks = int(timeline_weeks * discovery_pct / 100)
            phase2_weeks = int(timeline_weeks * validation_pct / 100)
            phase3_weeks = int(timeline_weeks * scaling_pct / 100)
        else:
            # Fallback to fixed values for backward compatibility
            phase_durations = project_exec.get('phase_durations', {})
            phase1_weeks = phase_durations.get('phase1_weeks', 16)
            phase2_weeks = phase_durations.get('phase2_weeks', 20)
            phase3_weeks = phase_durations.get('phase3_weeks', 16)
        
        # Calculate dynamic budget allocation with milestone unlocks
        capital_bounds = frontmatter.get('capital_bounds_bbd', {})
        min_capital = capital_bounds.get('min', 300000)
        
        budget_ratios = project_exec.get('budget_ratios', {}) or {}
        milestone_unlocks = project_exec.get('milestone_budget_unlocks', {}) or {}
        
        # Use new logic if project_execution section exists (even with empty budget_ratios)
        if project_exec:
            # Get capital bounds from brief
            capital_bounds = frontmatter.get('capital_bounds_bbd', {})
            min_capital_bound = capital_bounds.get('min', 300000)
            max_capital_bound = capital_bounds.get('max', 1000000)
            
            # Set investor-realistic capital boundaries
            discovery_min_capital = 250000  # $250K minimum for discovery phase
            max_total_capital = max_capital_bound  # Use brief's maximum capital bound
            
            # Use milestone-based capital with investor-realistic bounds
            if milestone_unlocks:
                initial_capital = max(discovery_min_capital, min(milestone_unlocks.get('initial', discovery_min_capital), max_total_capital))
                post_discovery_capital = max(initial_capital, min(milestone_unlocks.get('post_discovery', discovery_min_capital), max_total_capital))
                post_validation_capital = max(post_discovery_capital, min(milestone_unlocks.get('post_validation', discovery_min_capital), max_total_capital))
                max_capital = max(post_validation_capital, min(milestone_unlocks.get('post_scaling', discovery_min_capital), max_total_capital))
            else:
                # Use capital bounds when milestone_unlocks is empty
                capital_bounds = frontmatter.get('capital_bounds_bbd', {})
                min_capital_bound = capital_bounds.get('min', 300000)
                max_capital_bound = capital_bounds.get('max', 1000000)
                
                # Progressive capital unlocking based on validation milestones
                initial_capital = min_capital_bound  # Start with minimum
                post_discovery_capital = min(int(min_capital_bound * 1.67), max_total_capital)  # ~67% increase
                post_validation_capital = min(int(post_discovery_capital * 1.5), max_total_capital)  # ~50% increase  
                max_capital = min(max_capital_bound, max_total_capital)  # Respect both bounds
            
            # Investor-realistic capital allocation (risk-inverse funding)
            # Discovery: Lean validation - fail fast, fail cheap
            discovery_budget = min(75000, int(initial_capital * 0.30))  # Max $75K or 30% of initial
            
            # Validation: Prove business model - moderate investment after discovery success
            validation_budget = min(500000, int(post_discovery_capital * 0.40))  # Max $500K or 40% of unlocked capital
            
            # Scaling: Aggressive growth - major investment in proven winners
            scaling_budget = min(1000000, int(post_validation_capital * 0.50))  # Max $1M or 50% of unlocked capital
            
            # Ensure minimum viable budgets (balanced compromise)
            discovery_budget = max(discovery_budget, 150000)  # Min $150K for meaningful discovery
            validation_budget = max(validation_budget, 300000) # Min $300K for comprehensive validation
            scaling_budget = max(scaling_budget, 400000)      # Min $400K for substantial scaling impact
            
            # Investor principle: Total allocation cannot exceed available capital at each milestone
            if discovery_budget > initial_capital:
                discovery_budget = int(initial_capital * 0.90)  # Leave 10% buffer
            
            if validation_budget > (post_discovery_capital - discovery_budget):
                validation_budget = int((post_discovery_capital - discovery_budget) * 0.80)  # Leave 20% buffer
                
            if scaling_budget > (max_total_capital - discovery_budget - validation_budget):
                scaling_budget = int((max_total_capital - discovery_budget - validation_budget) * 0.75)  # Leave 25% buffer
            
            # Calculate totals
            phase1_2_budget = discovery_budget + validation_budget  # Combined for backward compatibility
            phase3_budget = scaling_budget
            total_budget = discovery_budget + validation_budget + scaling_budget
            
            # Set capital progression variables
            current_capital = initial_capital
        else:
            # Fallback to fixed values for backward compatibility
            budget_allocation = project_exec.get('budget_allocation', {})
            phase1_2_budget = budget_allocation.get('phase1_2_budget', 45000)
            phase3_budget = budget_allocation.get('phase3_budget', 30000)
            total_budget = budget_allocation.get('total_budget', 75000)
            current_capital = min_capital
            post_discovery_capital = min_capital
            post_validation_capital = min_capital
            max_capital = min_capital
        
        print(f"TEAM_SIZE='{team_size}'")
        print(f"PHASE1_WEEKS='{phase1_weeks}'")
        print(f"PHASE2_WEEKS='{phase2_weeks}'")
        print(f"PHASE3_WEEKS='{phase3_weeks}'")
        print(f"BMDP_DISCOVERY_COST='{discovery_budget}'")
        print(f"BMDP_VALIDATION_COST='{validation_budget}'")
        print(f"BMDP_PHASE1_2_COST='{phase1_2_budget}'")
        print(f"BMDP_SCALING_COST='{phase3_budget}'")
        print(f"TOTAL_BMDP_COST='{total_budget}'")
        
        # Output business capital available (funding for actual business operations)
        print(f"BUSINESS_INITIAL_CAPITAL='{current_capital}'")
        print(f"BUSINESS_POST_DISCOVERY_CAPITAL='{post_discovery_capital}'")
        print(f"BUSINESS_POST_VALIDATION_CAPITAL='{post_validation_capital}'")
        print(f"BUSINESS_MAX_CAPITAL='{max_capital}'")
        
        # Legacy variable names for backward compatibility
        print(f"DISCOVERY_BUDGET='{discovery_budget}'")
        print(f"VALIDATION_BUDGET='{validation_budget}'")
        print(f"PHASE1_2_BUDGET='{phase1_2_budget}'")
        print(f"PHASE3_BUDGET='{phase3_budget}'")
        print(f"TOTAL_BUDGET='{total_budget}'")
        print(f"INITIAL_CAPITAL='{current_capital}'")
        print(f"POST_DISCOVERY_CAPITAL='{post_discovery_capital}'")
        print(f"POST_VALIDATION_CAPITAL='{post_validation_capital}'")
        print(f"MAX_CAPITAL='{max_capital}'")
        
        # Output business model sections
        if 'value_proposition' in sections:
            value_prop = '. '.join(sections['value_proposition'])
            print(f"VALUE_PROPOSITION='{value_prop}'")
        
        if 'customer_segments' in sections:
            customers = '. '.join(sections['customer_segments'])
            print(f"CUSTOMER_SEGMENTS='{customers}'")
        
        if 'key_activities' in sections:
            activities = '. '.join(sections['key_activities'])
            print(f"KEY_ACTIVITIES='{activities}'")
        
        if 'key_resources' in sections:
            resources = '. '.join(sections['key_resources'])
            print(f"KEY_RESOURCES='{resources}'")
        
        if 'revenue_streams' in sections:
            revenue = '. '.join(sections['revenue_streams'])
            print(f"REVENUE_STREAMS='{revenue}'")
        
        if 'critical_risks' in sections:
            risks = '. '.join(sections['critical_risks'])
            print(f"CRITICAL_RISKS='{risks}'")
        
        if 'critical_risks' in sections:
            risks = '. '.join(sections['critical_risks'])
            print(f"CRITICAL_RISKS='{risks}'")
    
    return 0

if __name__ == '__main__':
    exit(main())
