#!/usr/bin/env python3
"""
Update Google Sheets CRM with seller data
"""

import json
import subprocess
import sys

def run_gog_command(command_parts):
    """Run gog command and return output"""
    cmd = ['gog'] + command_parts
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def update_cell(spreadsheet_id, range_str, account, *values):
    """Update cells with values"""
    cmd = ['sheets', 'update', spreadsheet_id, range_str, '--account', account] + list(values)
    stdout, stderr, rc = run_gog_command(cmd)
    if rc != 0:
        print(f"Error updating {range_str}: {stderr}")
        return False
    return True

def main():
    spreadsheet_id = '1VLUiuI46mP4EYtJ418bj9pgY4sQzrJqaNhhlvfILHC0'
    account = 'muchammadizzuddin@gmail.com'

    # Load sellers
    with open('/home/openclaw/.openclaw/workspace/output/market_research/sellers.json', 'r') as f:
        sellers = json.load(f)

    print("Updating CRM with seller data...")

    # Header row (already done)
    # Data rows
    for idx, seller in enumerate(sellers, start=2):
        print(f"Row {idx}: {seller['shop_name']}")

        # Calculate total value as IDR format
        total_value = f"IDR {seller['total_value']:,}"

        # Update cells individually
        # Column A: Shop Name
        update_cell(spreadsheet_id, f'Sheet1!A{idx}', account, seller['shop_name'])
        # Column B: Shop URL
        update_cell(spreadsheet_id, f'Sheet1!B{idx}', account, seller['shop_url'])
        # Column C: Total Sales
        update_cell(spreadsheet_id, f'Sheet1!C{idx}', account, str(seller['total_sales']))
        # Column D: Total Value
        update_cell(spreadsheet_id, f'Sheet1!D{idx}', account, total_value)
        # Column E: Avg Rating
        update_cell(spreadsheet_id, f'Sheet1!E{idx}', account, str(seller['avg_rating']))
        # Column F: Product
        if seller['products']:
            update_cell(spreadsheet_id, f'Sheet1!F{idx}', account, seller['products'][0]['product_name'])
        # Column G: Category
        if seller['products']:
            update_cell(spreadsheet_id, f'Sheet1!G{idx}', account, seller['products'][0]['category'])
        # Column H: Status
        update_cell(spreadsheet_id, f'Sheet1!H{idx}', account, 'Not Contacted')

    print("\nCRM update complete!")
    print(f"Spreadsheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")

if __name__ == '__main__':
    main()
