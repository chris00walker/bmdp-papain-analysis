#!/usr/bin/env python3
"""
Test-driven validation for grower business
Tests define expected behavior before implementation fixes
"""

import unittest
import csv
import json
import os
from pathlib import Path

class TestGrowerValidation(unittest.TestCase):
    
    def setUp(self):
        self.business_path = Path("businesses/grower")
        self.evidence_ledger_path = self.business_path / "evidence_ledger.csv"
        self.manifest_path = self.business_path / "manifest.json"
        self.financials_path = self.business_path / "30_design" / "financials_cashflow.csv"
    
    def test_evidence_ledger_exists_and_readable(self):
        """Test that evidence ledger exists and can be read without file handle issues"""
        self.assertTrue(self.evidence_ledger_path.exists(), "Evidence ledger must exist")
        
        # Test file can be opened and closed properly
        with open(self.evidence_ledger_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Test file handle is properly closed
        self.assertTrue(f.closed, "File handle must be closed after reading")
        
        # Test required headers exist
        required_headers = ['evidence_type', 'evidence_description', 'evidence_datum', 
                          'confidence', 'source_link', 'decision_impact', 'owner', 'date']
        
        with open(self.evidence_ledger_path, 'r') as f:
            reader = csv.DictReader(f)
            actual_headers = reader.fieldnames
            
        for header in required_headers:
            self.assertIn(header, actual_headers, f"Required header '{header}' missing")
    
    def test_financials_csv_schema(self):
        """Test that financials CSV has correct schema and valid data"""
        self.assertTrue(self.financials_path.exists(), "Financials CSV must exist")
        
        required_headers = ['year', 'revenues_bbd', 'capex_bbd', 'opex_bbd', 
                          'working_cap_change_bbd', 'notes']
        
        with open(self.financials_path, 'r') as f:
            reader = csv.DictReader(f)
            actual_headers = reader.fieldnames
            rows = list(reader)
        
        for header in required_headers:
            self.assertIn(header, actual_headers, f"Required header '{header}' missing")
        
        # Test CAPEX totals meet minimum requirements
        total_capex = sum(float(row['capex_bbd']) for row in rows)
        self.assertGreaterEqual(total_capex, 300000, "Total CAPEX must be >= 300,000 BBD")
        self.assertLessEqual(total_capex, 1000000, "Total CAPEX must be <= 1,000,000 BBD")
    
    def test_manifest_schema(self):
        """Test that manifest has required fields and structure"""
        self.assertTrue(self.manifest_path.exists(), "Manifest must exist")
        
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
        
        required_fields = ['business_slug', 'phases_completed', 'capital_bounds_bbd']
        
        for field in required_fields:
            self.assertIn(field, manifest, f"Required field '{field}' missing from manifest")
        
        # Test capital bounds structure
        capital_bounds = manifest['capital_bounds_bbd']
        self.assertIn('min', capital_bounds, "Capital bounds must have 'min' field")
        self.assertIn('max', capital_bounds, "Capital bounds must have 'max' field")
        self.assertEqual(capital_bounds['min'], 300000, "Min capital must be 300,000")
        self.assertEqual(capital_bounds['max'], 1000000, "Max capital must be 1,000,000")

if __name__ == '__main__':
    # Change to repo root for relative paths
    os.chdir('/home/chris/bmdp')
    unittest.main(verbosity=2)
