#!/usr/bin/env python3
"""
BMDP Business Validation Tool
Validates business structure, schemas, and capital bounds
"""

import argparse
import json
import csv
import os
import sys
from pathlib import Path
import yaml

class BMDPValidator:
    def __init__(self, business_slug: str, repo_root: str = "."):
        self.business_slug = business_slug
        self.repo_root = Path(repo_root)
        self.business_path = self.repo_root / "businesses" / business_slug
        self.errors = []
        self.warnings = []
        
    def validate_structure(self):
        """Validate required directory structure exists"""
        required_dirs = [
            "00_initiation",
            "10_mobilize", 
            "20_understand",
            "30_design"
        ]
        
        for dir_name in required_dirs:
            dir_path = self.business_path / dir_name
            if not dir_path.exists():
                self.errors.append(f"Missing required directory: {dir_path}")
                
    def validate_financials_csv(self):
        """Validate financials_cashflow.csv schema and capital bounds"""
        csv_path = self.business_path / "30_design" / "financials_cashflow.csv"
        
        if not csv_path.exists():
            self.errors.append(f"Missing required file: {csv_path}")
            return
            
        try:
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
            # Validate headers
            required_headers = ['year', 'capex_bbd', 'opex_bbd', 'revenues_bbd', 'working_cap_change_bbd', 'notes']
            actual_headers = reader.fieldnames
            
            for header in required_headers:
                if header not in actual_headers:
                    self.errors.append(f"Missing required column '{header}' in {csv_path}")
                    
            # Validate capital bounds (300k - 1M BBD)
            total_capex = 0
            for row in rows:
                try:
                    capex = float(row.get('capex_bbd', 0))
                    total_capex += capex
                except ValueError:
                    self.errors.append(f"Invalid capex_bbd value in {csv_path}: {row.get('capex_bbd')}")
                    
            if total_capex < 300000:
                self.errors.append(f"Total CAPEX ({total_capex:,.0f} BBD) below minimum 300,000 BBD")
            elif total_capex > 1000000:
                self.errors.append(f"Total CAPEX ({total_capex:,.0f} BBD) above maximum 1,000,000 BBD")
                
        except Exception as e:
            self.errors.append(f"Error reading {csv_path}: {str(e)}")
            
    def validate_evidence_ledger(self):
        """Validate evidence ledger schema"""
        csv_path = self.business_path / "evidence_ledger.csv"
        
        if not csv_path.exists():
            self.warnings.append(f"Missing evidence ledger: {csv_path}")
            return
            
        try:
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                
            required_headers = ['evidence_type', 'evidence_description', 'evidence_datum', 
                              'confidence', 'source_link', 'decision_impact', 'owner', 'date']
            actual_headers = reader.fieldnames
            
            for header in required_headers:
                if header not in actual_headers:
                    self.errors.append(f"Missing required column '{header}' in evidence ledger")
                    
        except Exception as e:
            self.errors.append(f"Error reading evidence ledger: {str(e)}")
            
    def validate_manifest(self):
        """Validate business manifest exists and has required fields"""
        manifest_path = self.business_path / "manifest.json"
        
        if not manifest_path.exists():
            self.errors.append(f"Missing business manifest: {manifest_path}")
            return
            
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                
            required_fields = ['business_slug', 'phases_completed', 'last_updated', 'capital_bounds_bbd']
            
            for field in required_fields:
                if field not in manifest:
                    self.errors.append(f"Missing required field '{field}' in manifest")
                    
        except Exception as e:
            self.errors.append(f"Error reading manifest: {str(e)}")
            
    def validate_brief_metadata(self):
        """Validate brief file has required YAML frontmatter"""
        brief_files = list(self.repo_root.glob(f"brief-*-{self.business_slug}.md"))
        
        if not brief_files:
            self.errors.append(f"No brief file found for business '{self.business_slug}'")
            return
            
        brief_path = brief_files[0]
        
        try:
            with open(brief_path, 'r') as f:
                content = f.read()
                
            if not content.startswith('---'):
                self.errors.append(f"Brief file missing YAML frontmatter: {brief_path}")
                return
                
            # Extract YAML frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                self.errors.append(f"Invalid YAML frontmatter format in: {brief_path}")
                return
                
            frontmatter = yaml.safe_load(parts[1])
            
            required_fields = ['business_slug', 'capital_bounds_bbd', 'financial_method']
            for field in required_fields:
                if field not in frontmatter:
                    self.errors.append(f"Missing required field '{field}' in brief frontmatter")
                    
        except Exception as e:
            self.errors.append(f"Error reading brief file: {str(e)}")
            
    def run_validation(self):
        """Run all validation checks"""
        print(f"Validating business: {self.business_slug}")
        print("=" * 50)
        
        self.validate_structure()
        self.validate_financials_csv()
        self.validate_evidence_ledger()
        self.validate_manifest()
        self.validate_brief_metadata()
        
        # Report results
        if self.errors:
            print(f"\n❌ VALIDATION FAILED ({len(self.errors)} errors)")
            for error in self.errors:
                print(f"  ERROR: {error}")
        else:
            print(f"\n✅ VALIDATION PASSED")
            
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)})")
            for warning in self.warnings:
                print(f"  WARNING: {warning}")
                
        return len(self.errors) == 0

def main():
    parser = argparse.ArgumentParser(description='Validate BMDP business structure and data')
    parser.add_argument('--business', required=True, help='Business slug to validate')
    parser.add_argument('--repo-root', default='.', help='Repository root path')
    
    args = parser.parse_args()
    
    validator = BMDPValidator(args.business, args.repo_root)
    success = validator.run_validation()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
