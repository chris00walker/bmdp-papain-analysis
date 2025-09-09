#!/usr/bin/env python3
"""
Update business manifest with validation and analysis results
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Update business manifest')
    parser.add_argument('--business', required=True, help='Business slug')
    parser.add_argument('--validation-status', default='passed', help='Validation status')
    
    args = parser.parse_args()
    
    manifest_path = Path(f'businesses/{args.business}/manifest.json')
    
    if not manifest_path.exists():
        print(f"❌ ERROR: Manifest not found: {manifest_path}")
        return 1
    
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        manifest['last_updated'] = datetime.now().isoformat() + 'Z'
        manifest['validation_status'] = args.validation_status
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f'✅ Manifest updated for {args.business}')
        return 0
        
    except Exception as e:
        print(f"❌ ERROR: Failed to update manifest: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
