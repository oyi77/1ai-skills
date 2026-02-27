# Google Sheets CRM Template for TikTok Content Agency

## Sheet Structure

### Sheet 1: Leads (Cold Email Outreach)

| Column | Header | Description |
|---------|---------|-------------|
| A | ID | Unique lead ID |
| B | Shop Name | Shopee shop name |
| C | Shop URL | Shopee shop URL |
| D | Total Sales | Total sales value (IDR) |
| E | Avg Rating | Average product rating |
| F | Num Products | Number of products |
| G | Email Status | Sent / Opened / Clicked / Replied |
| H | Email Date | Date cold email sent |
| I | Follow-up 1 | Date of first follow-up |
| J | Follow-up 2 | Date of second follow-up |
| K | Response | Yes / No / Pending |
| L | Meeting Date | Date meeting scheduled |
| M | Meeting Status | Scheduled / Completed / Cancelled |
| N | Sample Videos | Number of sample videos sent |
| O | Sample Date | Date sample videos sent |
| P | Conversion | Converted to client? Yes/No |
| Q | Package | Starter / Growth / Scale |
| R | Deal Value | Monthly deal value (IDR) |
| S | Notes | Additional notes |

### Sheet 2: Clients (Active Deals)

| Column | Header | Description |
|---------|---------|-------------|
| A | Client ID | Unique client ID |
| B | Shop Name | Shopee shop name |
| C | Contact Name | Main contact person |
| D | Email | Contact email |
| E | Phone | Contact phone |
| F | WhatsApp | WhatsApp number |
| G | Package | Starter / Growth / Scale |
| H | Monthly Fee | Monthly fee (IDR) |
| I | Start Date | Contract start date |
| J | End Date | Contract end date |
| K | Videos Generated | Total videos generated |
| L | Videos Posted | Total videos posted |
| M | Avg Engagement | Average engagement rate |
| D | Engagement Increase | % increase from baseline |
| E | Status | Active / On Hold / Cancelled |
| F | Cancel Reason | Reason for cancellation |
| G | LTV (Lifetime Value) | Total value of client (IDR) |
| H | Churn Risk | High / Medium / Low |
| I | Notes | Additional notes |

### Sheet 3: Video Performance

| Column | Header | Description |
|---------|---------|-------------|
| A | Video ID | Unique video ID |
| B | Client Name | Client name |
| C | Video Title | Video title/hook |
| D | Platform | TikTok / Facebook / Instagram |
| D | Posted Date | Date posted |
| E | Views | Total views |
| F | Likes | Total likes |
| G | Comments | Total comments |
| G | Shares | Total shares |
| H | Engagement Rate | Engagement % |
| I | Clicks | Link clicks |
| J | Conversions | Product purchases |
| K | Revenue | Revenue generated (IDR) |
| L | Cost | Video production cost (IDR) |
| M | ROI | Return on Investment |

### Sheet 4: Revenue Tracking

| Column | Header | Description |
|---------|---------|-------------|
| A | Date | Transaction date |
| B | Client Name | Client name |
| C | Package | Starter / Growth / Scale |
| D | Amount | Amount received (IDR) |
| E | Payment Method | Bank Transfer / E-Wallet / Credit Card |
| F | Status | Paid / Pending / Overdue |
| G | Invoice # | Invoice number |
| H | Invoice Date | Invoice date |
| I | Due Date | Payment due date |
| J | Notes | Notes |

### Sheet 5: Tasks & Follow-ups

| Column | Header | Description |
|---------|---------|-------------|
| A | Task ID | Unique task ID |
| B | Lead/Client ID | Related lead/client ID |
| C | Task Type | Cold Email / Follow-up / Meeting / Sample Video |
| D | Due Date | Due date |
| E | Status | Pending / In Progress / Completed / Cancelled |
| F | Priority | High / Medium / Low |
| G | Assigned To | Assigned person (Veris / Sony) |
| H | Notes | Notes |

---

## Sample Data (Sheet 1: Leads)

| ID | Shop Name | Shop URL | Total Sales | Avg Rating | Num Products | Email Status | Email Date | Response | Meeting Date | Package | Deal Value |
|----|-----------|----------|-------------|-------------|--------------|--------------|------------|-------------|------------|---------|------------|
| 1 | HomeFix Indonesia | https://shopee.co.id/shop/homefix | IDR 1.5B | 4.6 | 1 | Sent | 2026-02-27 | Pending | - | - | - |
| 2 | OrganizePro | https://shopee.co.id/shop/organizepro | IDR 1.4B | 4.8 | 1 | Sent | 2026-02-27 | Pending | - | - | - |
| 3 | TechDecor Official | https://shopee.co.id/shop/techdecor | IDR 1.2B | 4.8 | 1 | Sent | 2026-02-27 | Pending | - | - | - |

---

## Formulas

### Engagement Rate
`= (Likes + Comments + Shares) / Views * 100`

### ROI
`= (Revenue - Cost) / Cost * 100`

### Conversion Rate
`= Converted / Total Leads * 100`

### LTV (Lifetime Value)
`= Monthly Fee * Months Active`

---

## Automation with gogcli

### Create Lead Entry
```bash
gog sheets append "BerkahKarya CRM" "Leads" \
  --values "ID,Shop Name,Total Sales,Email Status" \
  --data "4,HomeFix Indonesia,1500000000,Sent"
```

### Update Lead Status
```bash
gog sheets update "BerkahKarya CRM" "Leads" \
  --row 2 \
  --values "Response,Meeting Date" \
  --data "Yes,2026-03-01"
```

### Export for Analysis
```bash
gog sheets export "BerkahKarya CRM" "Leads" \
  --format csv \
  --out leads_export.csv
```

---

*Last Updated: 2026-02-27*
*CRM Template for TikTok Content Agency*
