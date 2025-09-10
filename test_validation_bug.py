#!/usr/bin/env python3
"""
Test to reproduce and fix the validation script bug
"""

import unittest
import csv
from pathlib import Path

class TestValidationBugFix(unittest.TestCase):
    
    def test_csv_reader_file_handle_bug(self):
        """Test that reproduces the file handle bug in validation script"""
        csv_path = Path("businesses/grower/evidence_ledger.csv")
        
        # This is the BUGGY code from validate.py lines 84-89
        try:
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                # BUG: trying to access reader.fieldnames AFTER file is closed
            
            # This will fail because file handle is closed
            actual_headers = reader.fieldnames  # This causes "I/O operation on closed file"
            self.fail("Should have raised an exception")
            
        except ValueError as e:
            # This is the expected error we need to fix
            self.assertIn("I/O operation on closed file", str(e))
    
    def test_csv_reader_correct_implementation(self):
        """Test the CORRECT way to read CSV headers"""
        csv_path = Path("businesses/grower/evidence_ledger.csv")
        
        # CORRECT implementation: access fieldnames INSIDE the context manager
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            actual_headers = reader.fieldnames  # Access while file is still open
            rows = list(reader)  # Read data while file is open
        
        # Now we can use the data after file is closed
        required_headers = ['evidence_type', 'evidence_description', 'evidence_datum', 
                          'confidence', 'source_link', 'decision_impact', 'owner', 'date']
        
        for header in required_headers:
            self.assertIn(header, actual_headers, f"Required header '{header}' missing")
        
        self.assertGreater(len(rows), 0, "Should have data rows")

if __name__ == '__main__':
    import os
    os.chdir('/home/chris/bmdp')
    unittest.main(verbosity=2)
