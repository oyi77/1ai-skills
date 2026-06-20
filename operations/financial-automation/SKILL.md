---
name: financial-automation
description: AI CFO for solo businesses — invoicing, expense categorization, tax optimization, cash flow forecasting, multi-currency
  management
domain: operations
tags:
- automation
- business-ops
- financial
- management
- operations
---

## Overview

An AI-powered financial management system for solo entrepreneurs. Automates invoicing, categorizes expenses, forecasts cash flow, optimizes tax strategy, and generates financial reports. Connects to bank feeds via Plaid/Open Banking APIs to eliminate manual bookkeeping. Saves 5-10 hours per week for one-person companies.

## Required Tools

- **Bank Feeds**: Plaid API (US/EU) or TrueLayer (UK/EU) or GoCardless Bank Account Data
- **Invoicing**: Stripe Invoicing API or FreshBooks API
- **Accounting**: QuickBooks Online API or Xero API (optional)
- **Currency**: ExchangeRate-API or Open Exchange Rates
- **Reporting**: Python (pandas, matplotlib) or Node.js (chart.js)
- **Storage**: PostgreSQL or Google Sheets (simpler setups)
- **Notifications**: Email (SendGrid), Slack webhook

## Capabilities

- Connect to bank accounts and auto-import transactions
- Categorize expenses using AI (ML model or LLM)
- Generate and send professional invoices
- Track accounts receivable and send payment reminders
- Forecast cash flow 30/60/90 days out
- Multi-currency support with automatic conversion
- Generate quarterly and annual financial reports
- Detect anomalous transactions (fraud, duplicate charges)
- Tax optimization suggestions (deductions, timing)
- Export data for accountant/tax filing

## When to Use

- Monthly bookkeeping is taking too much time
- You need to track income/expenses across multiple accounts
- You want automated invoicing and payment reminders
- Cash flow forecasting for business decisions
- Quarterly tax prep and estimated tax calculations
- Multi-currency transactions need consolidation

## When NOT to Use

- Task is about financial analysis, not automation
- You need tax advice (consult a CPA)
- Task requires complex accounting (use accounting software)
- You're building financial software (use development skills)
- Task is about investment decisions (use financial skills)
- You don't have access to financial data sources

## Pseudo Code

Implementation patterns for common use cases with this skill.


### Phase 1: Bank Feed Connection

```python
# Plaid integration for bank account linking
import plaid
from plaid.api import plaid_api

configuration = plaid.Configuration(
    host=plaid.Environment.Production,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

client = plaid_api.PlaidApi(plaid.ApiClient(configuration))

# Create link token for bank connection
def create_link_token(user_id):
    request = LinkTokenCreateRequest(
        products=[Products('transactions')],
        client_name='AI CFO',
        country_codes=[CountryCode('US')],
        language='en',
        user=LinkTokenCreateRequestUser(client_user_id=user_id)
    )
    response = client.link_token_create(request)
    return response['link_token']

# Exchange public token for access token
def exchange_token(public_token):
    response = client.item_public_token_exchange(
        ItemPublicTokenExchangeRequest(public_token=public_token)
    )
    return response['access_token']

# Fetch transactions (run daily via cron)
def sync_transactions(access_token, start_date, end_date):
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date
    )
    response = client.transactions_get(request)
    return response['transactions']
```

### Phase 2: AI Expense Categorization

```python
# Categorize transactions using LLM
import openai

CATEGORIES = [
    "Software & Subscriptions", "Marketing & Advertising",
    "Travel & Transportation", "Meals & Entertainment",
    "Office Supplies", "Professional Services",
    "Equipment & Hardware", "Utilities & Telecom",
    "Income - Client Payment", "Income - Refund",
    "Tax Payment", "Bank Fees", "Other"
]

def categorize_transaction(transaction):
    prompt = f"""Categorize this business transaction into one of these categories:
    {CATEGORIES}

    Transaction: {transaction['name']}
    Amount: {transaction['amount']}
    Merchant: {transaction.get('merchant_name', 'Unknown')}

    Return only the category name."""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    category = response.choices[0].message.content.strip()

    # Store with confidence score
    return {
        "transaction_id": transaction['transaction_id'],
        "category": category,
        "confidence": "high",  # LLM-based, could add scoring
        "is_deductible": category not in ["Income - Client Payment", "Income - Refund", "Bank Fees"]
    }

# Batch categorize all uncategorized transactions
def categorize_all(transactions):
    categorized = []
    for txn in transactions:
        if txn['amount'] < 0:  # Expense
            result = categorize_transaction(txn)
            categorized.append(result)
    return categorized
```

### Phase 3: Invoicing

```python
# Generate and send invoices via Stripe
import stripe
stripe.api_key = STRIPE_SECRET_KEY

def create_invoice(client_email, client_name, line_items, due_days=30):
    # Create or retrieve customer
    customers = stripe.Customer.list(email=client_email)
    if customers.data:
        customer = customers.data[0]
    else:
        customer = stripe.Customer.create(
            email=client_email,
            name=client_name
        )

    # Create invoice
    invoice = stripe.Invoice.create(
        customer=customer.id,
        collection_method='send_invoice',
        days_until_due=due_days,
        metadata={"business_id": BUSINESS_ID}
    )

    # Add line items
    for item in line_items:
        stripe.InvoiceItem.create(
            customer=customer.id,
            invoice=invoice.id,
            amount=int(item['amount'] * 100),  # cents
            currency=item.get('currency', 'usd'),
            description=item['description']
        )

    # Send invoice
    stripe.Invoice.send_invoice(invoice.id)
    return invoice

# Payment reminder automation
def send_payment_reminders():
    overdue = stripe.Invoice.list(
        status='open',
        created={'lte': thirty_days_ago_timestamp}
    )
    for invoice in overdue.data:
        stripe.Invoice.send_invoice(invoice.id)
        notify_slack(f"Reminder sent: {invoice.customer_email} - ${invoice.amount_due/100}")
```

### Phase 4: Cash Flow Forecasting

```python
import pandas as pd
from datetime import datetime, timedelta

def forecast_cash_flow(transactions_df, days=90):
    """Forecast cash flow based on historical patterns."""

    # Calculate monthly averages
    monthly = transactions_df.resample('M', on='date').agg({
        'amount': ['sum', 'count', 'mean']
    })

    # Separate income and expenses
    income = transactions_df[transactions_df['amount'] > 0]
    expenses = transactions_df[transactions_df['amount'] < 0]

    avg_monthly_income = income.resample('M', on='date')['amount'].sum().mean()
    avg_monthly_expenses = abs(expenses.resample('M', on='date')['amount'].sum().mean())

    # Current balance
    current_balance = transactions_df['amount'].sum()

    # Project forward
    forecast = []
    running_balance = current_balance
    for day in range(1, days + 1):
        date = datetime.now() + timedelta(days=day)
        daily_income = avg_monthly_income / 30
        daily_expenses = avg_monthly_expenses / 30

        # Add seasonality (higher income at month end)
        if date.day >= 25:
            daily_income *= 1.5

        running_balance += daily_income - daily_expenses
        forecast.append({
            'date': date,
            'projected_balance': running_balance,
            'daily_income': daily_income,
            'daily_expenses': daily_expenses
        })

    return pd.DataFrame(forecast)
```

### Phase 5: Financial Reporting

```python
def generate_quarterly_report(transactions_df, quarter, year):
    """Generate quarterly financial report."""

    q_start = f"{year}-{(quarter-1)*3 + 1:02d}-01"
    q_end = f"{year}-{quarter*3:02d}-31"
    q_data = transactions_df[q_start:q_end]

    income = q_data[q_data['amount'] > 0]['amount'].sum()
    expenses = abs(q_data[q_data['amount'] < 0]['amount'].sum())
    net_profit = income - expenses

    # Category breakdown
    expense_by_category = q_data[q_data['amount'] < 0].groupby('category')['amount'].sum().abs()

    report = f"""
    # Q{quarter} {year} Financial Report

    ## Summary
    - Total Income: ${income:,.2f}
    - Total Expenses: ${expenses:,.2f}
    - Net Profit: ${net_profit:,.2f}
    - Profit Margin: {(net_profit/income)*100:.1f}%

    ## Top Expense Categories
    {expense_by_category.sort_values(ascending=False).head(5).to_string()}

    ## Deductible Expenses
    - Total Deductible: ${q_data[q_data['is_deductible']]['amount'].sum():,.2f}

    ## Estimated Tax (Quarterly)
    - Federal (25%): ${net_profit * 0.25:,.2f}
    - Self-Employment (15.3%): ${net_profit * 0.153:,.2f}
    """

    return report
```

### Phase 6: Anomaly Detection

```python
def detect_anomalies(transactions_df, std_threshold=2.5):
    """Flag unusual transactions."""

    # Calculate per-category statistics
    stats = transactions_df.groupby('category')['amount'].agg(['mean', 'std'])

    anomalies = []
    for _, txn in transactions_df.iterrows():
        cat_stats = stats.loc[txn['category']]
        z_score = abs(txn['amount'] - cat_stats['mean']) / cat_stats['std']

        if z_score > std_threshold:
            anomalies.append({
                'transaction': txn,
                'reason': f"Amount ${txn['amount']:.2f} is {z_score:.1f} std devs from {txn['category']} average",
                'severity': 'high' if z_score > 3 else 'medium'
            })

    # Check for duplicates
    duplicates = transactions_df[
        transactions_df.duplicated(subset=['amount', 'merchant_name'], keep=False)
    ]
    for _, dup in duplicates.iterrows():
        anomalies.append({
            'transaction': dup,
            'reason': f"Possible duplicate: ${dup['amount']:.2f} at {dup['merchant_name']}",
            'severity': 'medium'
        })

    return anomalies
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Plaid `ITEM_LOGIN_REQUIRED` | Bank credentials expired | Re-authenticate via Plaid Link |
| Plaid `INVALID_CREDENTIALS` | Wrong bank login | Verify credentials, check 2FA requirements |
| Stripe invoice 400 | Invalid customer email | Validate email format before creating invoice |
| Currency conversion mismatch | Stale exchange rates | Cache rates with 1-hour TTL, fallback to last known rate |
| Duplicate transactions | Plaid sync overlap | Use `transaction_id` deduplication before storing |
| Missing categorization | LLM timeout | Retry with exponential backoff, fallback to "Other" category |

## Common Patterns

Reusable patterns that appear frequently when applying this skill.


### Multi-Account Consolidation
```python
# Merge transactions from multiple bank accounts
def consolidate_accounts(access_tokens):
    all_transactions = []
    for token in access_tokens:
        txns = sync_transactions(token, start_date, end_date)
        all_transactions.extend(txns)
    return pd.DataFrame(all_transactions).sort_values('date')
```

### Auto-Recurring Detection
```python
def detect_recurring(df, min_occurrences=3):
    """Find subscription/recurring payments."""
    grouped = df.groupby(['merchant_name', 'amount']).size()
    recurring = grouped[grouped >= min_occurrences].reset_index()
    return recurring
```

### Monthly Close Process
```python
def monthly_close(year, month):
    txns = fetch_month(year, month)
    categorize_all(txns)
    anomalies = detect_anomalies(txns)
    report = generate_monthly_report(txns)
    send_report_email(report)
    archive_month(year, month, txns)
```

## Red Flags

- Not reconciling financial data
- Ignoring tax compliance requirements
- Missing audit trails
- Not backing up financial data
- Ignoring financial regulations

## Verification

- [ ] Financial data is reconciled
- [ ] Tax compliance is maintained
- [ ] Audit trails are in place
- [ ] Financial data is backed up
- [ ] Financial regulations are followed

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
