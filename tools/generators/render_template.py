#!/usr/bin/env python3
"""
Template Renderer - CLI wrapper for adaptive template rendering
"""

import sys
import argparse
from pathlib import Path
sys.path.append('/home/chris/bmdp')

from tools.generators.adaptive_template_renderer import AdaptiveTemplateRenderer

def main():
    parser = argparse.ArgumentParser(description='Render Jinja2 templates with business context')
    parser.add_argument('--template', required=True, help='Template path relative to templates/')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--business', help='Business name (auto-detected from output path if not provided)')
    
    args = parser.parse_args()
    
    # Auto-detect business from output path if not provided
    business = args.business
    if not business:
        output_path = Path(args.output)
        if 'businesses' in output_path.parts:
            business_idx = output_path.parts.index('businesses')
            if business_idx + 1 < len(output_path.parts):
                business = output_path.parts[business_idx + 1]
    
    if not business:
        print("Error: Could not determine business name", file=sys.stderr)
        return 1
    
    # Create renderer
    renderer = AdaptiveTemplateRenderer(business)
    
    # Render template
    template_path = Path('/home/chris/bmdp/templates') / args.template
    if renderer.render_template(str(template_path), args.output):
        print(f"✅ Rendered {args.template} -> {args.output}")
        return 0
    else:
        print(f"❌ Failed to render {args.template}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
