#!/usr/bin/env python3
"""
Prototype: Dynamic Variable Generation Framework
On-demand variable generation with business model pattern matching
"""

from typing import Dict, Set, Any
import random

class DynamicVariableGenerator:
    """Framework that generates variables on-demand based on template requirements"""
    
    def __init__(self):
        self.generation_strategies = {
            'financial': self._generate_financial_variable,
            'team': self._generate_team_variable,
            'risk': self._generate_risk_variable,
            'timeline': self._generate_timeline_variable,
            'market': self._generate_market_variable,
            'operational': self._generate_operational_variable,
            'strategic': self._generate_strategic_variable
        }
        
        # Business model patterns for intelligent defaults
        self.business_models = {
            'agriculture': {
                'revenue_multiple': 0.25,
                'margin_range': (0.15, 0.25),
                'growth_rate': 0.08,
                'risk_profile': 'medium-high',
                'capital_intensity': 'high',
                'seasonality': True
            },
            'manufacturing': {
                'revenue_multiple': 0.35,
                'margin_range': (0.20, 0.35),
                'growth_rate': 0.12,
                'risk_profile': 'medium',
                'capital_intensity': 'high',
                'seasonality': False
            },
            'technology': {
                'revenue_multiple': 0.45,
                'margin_range': (0.60, 0.80),
                'growth_rate': 0.35,
                'risk_profile': 'high',
                'capital_intensity': 'low',
                'seasonality': False
            },
            'services': {
                'revenue_multiple': 0.40,
                'margin_range': (0.25, 0.45),
                'growth_rate': 0.15,
                'risk_profile': 'low-medium',
                'capital_intensity': 'low',
                'seasonality': False
            }
        }
    
    def generate_variables(self, business_data: Dict, required_vars: Set[str]) -> Dict[str, str]:
        """Generate variables using dynamic framework approach"""
        
        # Determine business model pattern
        business_pattern = self._identify_business_pattern(business_data)
        model_config = self.business_models.get(business_pattern, self.business_models['manufacturing'])
        
        generated_vars = {}
        
        for var in required_vars:
            # Categorize variable and use appropriate generation strategy
            category = self._categorize_variable(var)
            strategy = self.generation_strategies.get(category, self._generate_default_variable)
            
            generated_vars[var] = strategy(var, business_data, model_config)
        
        return generated_vars
    
    def _identify_business_pattern(self, business_data: Dict) -> str:
        """Identify business model pattern from data"""
        industry = business_data.get('industry_context', '').lower()
        business_type = business_data.get('business_type', '').lower()
        
        if any(term in industry for term in ['agriculture', 'farming', 'cultivation']):
            return 'agriculture'
        elif any(term in business_type for term in ['technology', 'software', 'platform', 'digital']):
            return 'technology'
        elif any(term in business_type for term in ['service', 'consulting', 'advisory']):
            return 'services'
        else:
            return 'manufacturing'
    
    def _categorize_variable(self, var: str) -> str:
        """Categorize variable to determine generation strategy"""
        var_lower = var.lower()
        
        if any(term in var_lower for term in ['budget', 'cost', 'revenue', 'capital', 'funding', 'price']):
            return 'financial'
        elif any(term in var_lower for term in ['team', 'lead', 'manager', 'analyst', 'role']):
            return 'team'
        elif any(term in var_lower for term in ['risk', 'probability', 'impact', 'mitigation']):
            return 'risk'
        elif any(term in var_lower for term in ['timeline', 'weeks', 'months', 'date', 'schedule']):
            return 'timeline'
        elif any(term in var_lower for term in ['market', 'competitive', 'customer', 'segment']):
            return 'market'
        elif any(term in var_lower for term in ['tech', 'operational', 'regulatory', 'partnership']):
            return 'operational'
        else:
            return 'strategic'
    
    def _generate_financial_variable(self, var: str, business_data: Dict, model_config: Dict) -> str:
        """Generate financial variables with business model intelligence"""
        var_lower = var.lower()
        capital_min = business_data.get('capital_min', 750000)
        
        if 'market_size' in var_lower:
            market_multiple = 8 if model_config['capital_intensity'] == 'low' else 5
            market_size = capital_min * market_multiple
            return f"${market_size:,} addressable market"
            
        elif 'acquisition_cost' in var_lower:
            if model_config['capital_intensity'] == 'low':
                return "$50-100 per customer (digital channels)"
            else:
                return "$150-250 per customer (relationship-based)"
                
        elif 'y1_revenue' in var_lower:
            revenue = int(capital_min * model_config['revenue_multiple'])
            return f"${revenue:,}"
            
        elif 'funding_requirements' in var_lower:
            multiplier = 2.5 if model_config['capital_intensity'] == 'low' else 4.0
            funding = int(capital_min * multiplier)
            return f"${funding:,} for operations and growth"
            
        elif 'budget' in var_lower:
            base_budget = int(capital_min * 0.15)
            if 'discovery' in var_lower:
                return f"${int(base_budget * 0.35):,}"
            elif 'validation' in var_lower:
                return f"${int(base_budget * 0.40):,}"
            elif 'scaling' in var_lower:
                return f"${int(base_budget * 0.25):,}"
            else:
                return f"${base_budget:,}"
        
        return f"${random.randint(10000, 100000):,}"
    
    def _generate_team_variable(self, var: str, business_data: Dict, model_config: Dict) -> str:
        """Generate team-related variables"""
        business_type = business_data.get('business_type', 'Business')
        
        if 'team_lead' in var.lower():
            return f"Senior {business_type} Business Lead"
        elif 'project_manager' in var.lower():
            if model_config['capital_intensity'] == 'low':
                return "Agile Product Manager"
            else:
                return "Operations Project Manager"
        elif 'analyst' in var.lower():
            return f"{business_type} Domain Analyst"
        
        return f"Experienced team member with {business_type.lower()} expertise"
    
    def _generate_risk_variable(self, var: str, business_data: Dict, model_config: Dict) -> str:
        """Generate risk assessment variables"""
        var_lower = var.lower()
        
        # Risk scenarios by business model
        risk_scenarios = {
            'agriculture': ["Weather and climate dependency", "Market price volatility", "Regulatory compliance"],
            'technology': ["Platform scalability challenges", "User acquisition costs", "Competitive disruption"],
            'manufacturing': ["Supply chain disruption", "Quality control issues", "Equipment maintenance"],
            'services': ["Client concentration risk", "Talent retention", "Market demand shifts"]
        }
        
        business_pattern = self._identify_business_pattern(business_data)
        risks = risk_scenarios.get(business_pattern, risk_scenarios['manufacturing'])
        
        if 'risk_1' in var_lower:
            return risks[0]
        elif 'risk_2' in var_lower:
            return risks[1]
        elif 'risk_3' in var_lower:
            return risks[2] if len(risks) > 2 else "Operational execution challenges"
        elif 'probability' in var_lower:
            return model_config['risk_profile'].split('-')[0].title()
        elif 'impact' in var_lower:
            return "High" if model_config['risk_profile'] == 'high' else "Medium"
        
        return "Standard business risk mitigation"
    
    def _generate_timeline_variable(self, var: str, business_data: Dict, model_config: Dict) -> str:
        """Generate timeline-related variables"""
        var_lower = var.lower()
        
        # Base timeline adjustments by business model
        base_weeks = 52
        if model_config['seasonality']:
            base_weeks = 78  # Longer for seasonal businesses
        elif model_config['capital_intensity'] == 'low':
            base_weeks = 39  # Faster for low-capital businesses
        
        if 'total_timeline' in var_lower:
            return f"{base_weeks} weeks"
        elif 'gtm_timeline' in var_lower:
            gtm_weeks = int(base_weeks * 0.6)
            return f"{gtm_weeks} weeks from project initiation"
        elif 'weeks' in var_lower:
            return f"{random.randint(4, 16)} weeks"
        
        return "TBD - Timeline to be determined during planning"
    
    def _generate_market_variable(self, var: str, business_data: Dict, model_config: Dict) -> str:
        """Generate market-related variables"""
        var_lower = var.lower()
        business_type = business_data.get('business_type', 'Business')
        
        if 'competitive_position' in var_lower:
            if model_config['capital_intensity'] == 'high':
                return f"Differentiated {business_type.lower()} with operational excellence focus"
            else:
                return f"Agile {business_type.lower()} with innovation advantage"
        elif 'customer' in var_lower:
            return f"Target customers in {business_type.lower()} value chain"
        elif 'market' in var_lower:
            growth = int(model_config['growth_rate'] * 100)
            return f"Growing market with {growth}% annual expansion"
        
        return f"Market-appropriate strategy for {business_type.lower()} sector"
    
    def _generate_operational_variable(self, var: str, business_data: Dict, model_config: Dict) -> str:
        """Generate operational variables"""
        var_lower = var.lower()
        business_type = business_data.get('business_type', 'Business')
        
        if 'tech_requirements' in var_lower:
            if model_config['capital_intensity'] == 'low':
                return "Cloud-based systems, automation tools, analytics platform"
            else:
                return "Industrial systems, quality control, inventory management"
        elif 'regulatory' in var_lower:
            return f"Industry-standard compliance for {business_type.lower()} operations"
        elif 'partnership' in var_lower:
            return f"Strategic partnerships in {business_type.lower()} ecosystem"
        
        return f"Operational requirements for {business_type.lower()} business"
    
    def _generate_strategic_variable(self, var: str, business_data: Dict, model_config: Dict) -> str:
        """Generate strategic variables"""
        var_lower = var.lower()
        business_type = business_data.get('business_type', 'Business')
        
        if 'exit_strategy' in var_lower:
            if model_config['growth_rate'] > 0.25:
                return "High-growth exit via strategic acquisition or IPO (5-7 years)"
            else:
                return "Stable business exit via management buyout or strategic sale (7-10 years)"
        elif 'success_criteria' in var_lower:
            if '1' in var:
                return "Achieve sustainable competitive advantage"
            elif '2' in var:
                return f"Establish profitable operations with {int(model_config['margin_range'][0]*100)}%+ margins"
            elif '3' in var:
                return "Build scalable business model for long-term growth"
        
        return f"Strategic initiative for {business_type.lower()} business development"
    
    def _generate_default_variable(self, var: str, business_data: Dict, model_config: Dict) -> str:
        """Default variable generation fallback"""
        business_type = business_data.get('business_type', 'Business')
        return f"Context-appropriate {var.lower().replace('_', ' ')} for {business_type.lower()} business"
