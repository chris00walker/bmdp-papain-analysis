#!/usr/bin/env python3
"""
BMDP Currency Conversion Tool
Standardizes all financial data to BBD with explicit conversion rates
"""

import argparse
import json
from pathlib import Path

# Fixed exchange rates (update as needed)
EXCHANGE_RATES = {
    'USD_TO_BBD': 2.00,  # 1 USD = 2 BBD (fixed peg)
    'EUR_TO_BBD': 2.20,  # Approximate
    'GBP_TO_BBD': 2.50,  # Approximate
    'CAD_TO_BBD': 1.50,  # Approximate
}

def convert_to_bbd(amount, from_currency='USD'):
    """Convert amount from specified currency to BBD"""
    if from_currency == 'BBD':
        return amount
    
    rate_key = f"{from_currency}_TO_BBD"
    if rate_key not in EXCHANGE_RATES:
        raise ValueError(f"Unsupported currency: {from_currency}")
    
    return amount * EXCHANGE_RATES[rate_key]

def save_conversion_log(business_slug, conversions, repo_root='.'):
    """Save currency conversion log for audit trail"""
    log_path = Path(repo_root) / "businesses" / business_slug / "currency_conversions.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_path, 'w') as f:
        json.dump({
            'exchange_rates_used': EXCHANGE_RATES,
            'conversions': conversions,
            'note': 'All financial data standardized to BBD'
        }, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Convert financial data to BBD standard')
    parser.add_argument('--business', required=True, help='Business slug')
    parser.add_argument('--from-currency', default='USD', help='Source currency')
    parser.add_argument('--amount', type=float, help='Amount to convert')
    parser.add_argument('--repo-root', default='.', help='Repository root path')
    
    args = parser.parse_args()
    
    if args.amount:
        # Single conversion
        bbd_amount = convert_to_bbd(args.amount, args.from_currency)
        print(f"{args.amount:,.2f} {args.from_currency} = {bbd_amount:,.2f} BBD")
        print(f"Exchange rate used: 1 {args.from_currency} = {EXCHANGE_RATES.get(f'{args.from_currency}_TO_BBD', 'N/A')} BBD")
    else:
        # Display current rates
        print("Current Exchange Rates to BBD:")
        print("=" * 30)
        for rate_key, rate in EXCHANGE_RATES.items():
            currency = rate_key.split('_')[0]
            print(f"1 {currency} = {rate} BBD")

if __name__ == '__main__':
    main()
