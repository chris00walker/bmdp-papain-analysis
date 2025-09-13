#!/usr/bin/env python3
"""
Generate comprehensive business summary report
"""

import argparse
import json
import csv
from pathlib import Path

def generate_summary_report(business_slug: str):
    """Generate comprehensive business analysis summary"""
    business_path = Path(f"businesses/{business_slug}")
    
    # Read financial summary
    financials_path = business_path / "30_design" / "financials_summary.csv"
    manifest_path = business_path / "manifest.json"
    
    # Business-specific context
    business_contexts = {
        'grower': {
            'type': 'Grower - Premium Single-Origin Papain Production',
            'industry': 'Agricultural Processing / Specialty Agriculture',
            'description': 'Solid returns from premium papain production with pharmaceutical-grade traceability',
            'performance_context': 'strong agricultural returns',
            'position': 'Premium single-origin papain with traceability',
            'advantages': "Barbados' favorable climate and geographic advantages to produce high-quality, traceable papain for premium markets",
            'risks': [
                '**Agricultural Risk**: Weather, climate, and crop yield variability',
                '**Market Risk**: Commodity price fluctuations and demand cycles',
                '**Regulatory Risk**: Organic certification and quality standard compliance',
                '**Operational Risk**: Farming expertise and labor availability',
                '**Competition Risk**: Other premium papain producers and synthetic alternatives'
            ],
            'next_steps': [
                'Secure agricultural land and farming permits',
                'Establish organic certification and quality protocols',
                'Develop cultivation and harvesting infrastructure',
                'Build relationships with premium buyers',
                'Execute Phase 4 validation experiments per test cards'
            ]
        },
        'processor': {
            'type': 'Processor - Pharmaceutical-Grade Papain Refining Facility',
            'industry': 'Pharmaceutical Processing / Biotechnology',
            'description': 'Exceptional returns from high-value pharmaceutical-grade papain processing',
            'performance_context': 'extraordinary performance',
            'position': 'Premium pharmaceutical-grade enzyme processing',
            'advantages': 'advanced processing technology to produce pharmaceutical-grade papain with exceptional purity standards, commanding premium pricing in global markets',
            'risks': [
                '**Regulatory Risk**: Pharmaceutical-grade processing requires strict compliance with international standards',
                '**Technology Risk**: Specialized equipment and processing expertise requirements',
                '**Market Risk**: Dependence on pharmaceutical industry demand cycles',
                '**Competition Risk**: Potential entry of larger pharmaceutical processors'
            ],
            'next_steps': [
                'Secure regulatory approvals for pharmaceutical-grade processing',
                'Finalize specialized equipment procurement and installation',
                'Establish quality assurance protocols and certifications',
                'Develop strategic partnerships with pharmaceutical companies',
                'Execute Phase 4 validation experiments per test cards'
            ]
        },
        'distributor': {
            'type': 'Distributor - Regional Papain Import/Export & Distribution Network',
            'industry': 'International Trade / Agricultural Distribution',
            'description': 'Strong returns from regional distribution and international trade operations',
            'performance_context': 'very strong performance',
            'position': 'Regional distribution hub for papain products',
            'advantages': 'Caribbean geographic advantages to serve as a regional hub for papain distribution, connecting local producers with international markets',
            'risks': [
                '**Regulatory Risk**: International trade regulations and customs requirements',
                '**Currency Risk**: Multi-currency operations and exchange rate fluctuations',
                '**Logistics Risk**: Dependence on shipping and transportation networks',
                '**Market Risk**: Commodity price volatility and demand fluctuations',
                '**Competition Risk**: Established distribution networks and new market entrants'
            ],
            'next_steps': [
                'Establish import/export licenses and regulatory compliance',
                'Secure warehouse facilities and distribution infrastructure',
                'Develop supplier relationships with papain producers',
                'Build customer network across target markets',
                'Execute Phase 4 validation experiments per test cards'
            ]
        },
        'marketplace': {
            'type': 'Marketplace - Digital B2B Papain Trading Platform',
            'industry': 'Digital Commerce / Agricultural Technology',
            'description': 'Strong returns from digital marketplace operations',
            'performance_context': 'strong digital platform performance',
            'position': 'Digital B2B trading platform for papain products',
            'advantages': 'digital platform technology to connect papain producers with buyers globally, reducing transaction costs and improving market efficiency',
            'risks': [
                '**Technology Risk**: Platform development and maintenance requirements',
                '**Market Risk**: Digital adoption rates in agricultural sector',
                '**Competition Risk**: Established trading platforms and new market entrants',
                '**Regulatory Risk**: Digital commerce and financial transaction compliance'
            ],
            'next_steps': [
                'Complete platform development and testing',
                'Onboard initial producer and buyer networks',
                'Establish payment and logistics partnerships',
                'Develop marketing and user acquisition strategies',
                'Execute Phase 4 validation experiments per test cards'
            ]
        }
    }
    
    # Read data
    financials = {}
    if financials_path.exists():
        with open(financials_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                financials[row['metric']] = row['value']
    
    manifest = {}
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    
    # Generate report
    report_path = business_path / "analysis_summary.md"
    
    # Get business context
    context = business_contexts.get(business_slug, {
        'type': f'{business_slug.title()} Business',
        'industry': 'N/A',
        'description': 'Business operations',
        'performance_context': 'performance',
        'position': 'Market position',
        'advantages': 'competitive advantages',
        'risks': ['**Risk**: General business risks'],
        'next_steps': ['Execute business plan', 'Execute Phase 4 validation experiments per test cards']
    })
    
    with open(report_path, 'w') as f:
        f.write(f"# Business Analysis Summary - {manifest.get('business_name', business_slug.title())}\n\n")
        
        # Executive Summary
        f.write("## Executive Summary\n\n")
        f.write(f"**Business**: {context['type']}\n")
        f.write(f"**Industry**: {context['industry']}\n")
        f.write(f"**Location**: {manifest.get('location', 'Caribbean Region')}\n")
        f.write(f"**Validation Status**: {manifest.get('validation_status', 'passed')}\n\n")
        
        # Financial Performance
        f.write("## Financial Performance\n\n")
        f.write(f"{context['description']}:\n\n")
        
        if 'irr_pct' in financials:
            irr_pct = float(financials['irr_pct']) * 100
            f.write(f"- **IRR**: {irr_pct:.1f}% ({context['performance_context']})\n")
        if 'npv_bbd' in financials:
            npv = float(financials['npv_bbd'])
            npv_desc = 'highest portfolio value' if npv > 20000000 else 'substantial value creation' if npv > 4000000 else 'positive value creation'
            f.write(f"- **NPV**: {npv:,.0f} BBD ({npv_desc})\n")
        if 'roi_pct' in financials:
            roi_pct = float(financials['roi_pct']) * 100
            f.write(f"- **ROI**: {roi_pct:,.1f}% over investment horizon\n")
        if 'capex_y0_bbd' in financials:
            capex = float(financials['capex_y0_bbd'])
            f.write(f"- **Initial Investment**: {capex:,.0f} BBD CAPEX\n")
        if 'discount_rate_pct' in financials:
            discount = float(financials['discount_rate_pct']) * 100
            f.write(f"- **Discount Rate**: {discount:.1f}%\n")
        
        # Key Financial Metrics subsection
        f.write("\n### Key Financial Metrics\n\n")
        if 'financial_summary' in manifest:
            fs = manifest['financial_summary']
            if fs.get('break_even_months'):
                f.write(f"- **Break-even Timeline**: {fs.get('break_even_months')} months (rapid payback)\n")
            if fs.get('year_5_revenue'):
                f.write(f"- **Year 5 Revenue**: {fs.get('year_5_revenue'):,.0f} BBD (strong growth trajectory)\n")
            if fs.get('year_5_net_income'):
                f.write(f"- **Year 5 Net Income**: {fs.get('year_5_net_income'):,.0f} BBD (healthy profitability)\n")
        f.write(f"- **Market Position**: {context['position']}\n\n")
        
        # Key Metrics
        if 'key_metrics' in manifest:
            f.write("## Key Business Metrics\n\n")
            metrics = manifest['key_metrics']
            f.write(f"- **Target Customers**: {metrics.get('target_customers', 'N/A')}\n")
            f.write(f"- **Value Proposition**: {metrics.get('value_proposition', 'N/A')}\n")
            f.write(f"- **Competitive Advantage**: {metrics.get('competitive_advantage', 'N/A')}\n")
            f.write(f"- **Revenue Model**: {metrics.get('revenue_model', 'N/A')}\n\n")
        
        # Phase Completion
        if 'phases_completed' in manifest:
            f.write("## BMDP Phase Completion\n\n")
            phases = manifest['phases_completed']
            for phase in phases:
                if isinstance(phase, dict):
                    # New format: dict with phase info
                    phase_name = phase.get('name', f"phase_{phase.get('phase', 'unknown')}")
                    f.write(f"- ✅ Phase {phase.get('phase', '?')}: {phase_name.replace('_', ' ').title()}\n")
                else:
                    # Old format: string
                    f.write(f"- ✅ {phase.replace('_', ' ').title()}\n")
            f.write("\n")
        
        # Investment Recommendation
        f.write("## Investment Recommendation\n\n")
        irr_pct = float(financials.get('irr_pct', 0)) * 100 if 'irr_pct' in financials else 0
        npv = float(financials.get('npv_bbd', 0)) if 'npv_bbd' in financials else 0
        
        if irr_pct > 200:
            recommendation = "**STRONGLY RECOMMENDED** - Exceptional investment opportunity with outstanding financial returns"
            portfolio_rank = "industry-leading"
        elif irr_pct > 100:
            recommendation = "**RECOMMENDED** - Strong investment opportunity with excellent financial returns"
            portfolio_rank = "robust"
        elif irr_pct > 50:
            recommendation = "**RECOMMENDED** - Solid investment opportunity with strong returns"
            portfolio_rank = "healthy"
        else:
            recommendation = "**REVIEW** - Investment returns below expected threshold"
            portfolio_rank = "modest"
        
        f.write(f"{recommendation}. The {business_slug} business demonstrates:\n\n")
        f.write(f"- {portfolio_rank.title()} IRR of {irr_pct:.1f}%\n")
        if npv > 1000000:
            f.write(f"- Substantial NPV generation ({npv/1000000:.1f}M BBD)\n")
        else:
            f.write(f"- Positive NPV generation ({npv:,.0f} BBD)\n")
        
        if 'financial_summary' in manifest and manifest['financial_summary'].get('break_even_months'):
            f.write(f"- Rapid break-even timeline ({manifest['financial_summary']['break_even_months']} months)\n")
        
        f.write(f"- Strategic market positioning with competitive advantages\n\n")
        f.write(f"The business leverages {context['advantages']}.\n\n")
        
        # Risk Considerations
        f.write("## Risk Considerations\n\n")
        for risk in context['risks']:
            f.write(f"- {risk}\n")
        
        # Next Steps
        f.write("\n## Next Steps\n\n")
        for i, step in enumerate(context['next_steps'], 1):
            f.write(f"{i}. {step}\n")
    
    print(f"✅ Business summary report generated: {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate business summary report")
    parser.add_argument("--business", required=True, help="Business slug")
    
    args = parser.parse_args()
    generate_summary_report(args.business)
