---
name: invoice-automation
description: Automate invoice processing, accounts payable, payment reminders, and financial reconciliation using AI. Extract data from PDF invoices, auto-categorize expenses, match POs, send payment reminders. Use when: business processes 10+ invoices/month manually, needs automated payment reminders, wants expense tracking from receipts/emails. Revenue: $1,000–10,000/client/month. Triggers on "invoice automation", "AP automation", "accounts payable", "payment reminder", "receipt scanning", "expense automation".
---

# Invoice & AP Automation

## Overview

Automate the entire invoice lifecycle: receive → extract → validate → approve → pay → reconcile. Eliminate manual data entry and late payment penalties.

**Pain**: Indonesian SMBs lose 8–15 hours/week on manual invoice processing  
**Value**: 70–80% time reduction, zero late payment penalties  
**Revenue**: IDR 2M–15M/client/month  

---

## When to Use

- Business processes 10+ invoices per week
- Manual entry into accounting software (Accurate, Jurnal, QuickBooks)
- Missing payment deadlines due to manual tracking
- Reconciling bank statements against invoices
- Scanning physical receipts for expense claims
- Sending payment reminders to customers

---

## Core Pipeline

```
Step 1: Receive invoice (email attachment / WhatsApp / upload)
Step 2: Extract data (OCR + AI)
Step 3: Validate (match PO, check amounts)
Step 4: Route for approval (if above threshold)
Step 5: Record in accounting software
Step 6: Send to payment queue
Step 7: Auto-send payment reminders
Step 8: Reconcile with bank statement
```

---

## Tech Stack

### OCR + Extraction
```python
# pip install pytesseract pdf2image pillow anthropic
# Option A: Local Tesseract (free)
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

def extract_invoice_data_ocr(pdf_path: str) -> str:
    """Extract text from PDF invoice using OCR"""
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang="ind+eng")
    return text

# Option B: Claude Vision (accurate, handles Indonesian)
import anthropic
import base64

def extract_invoice_data_claude(pdf_path: str) -> dict:
    """Extract structured data from invoice using Claude"""
    client = anthropic.Anthropic()
    
    with open(pdf_path, "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode()
    
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_data}
                },
                {
                    "type": "text",
                    "text": """Extract invoice data as JSON:
{
  "vendor_name": "",
  "invoice_number": "",
  "invoice_date": "",
  "due_date": "",
  "subtotal": 0,
  "tax": 0,
  "total": 0,
  "currency": "IDR",
  "line_items": [{"description": "", "qty": 0, "unit_price": 0, "amount": 0}],
  "bank_account": "",
  "notes": ""
}"""
                }
            ]
        }]
    )
    
    import json, re
    text = response.content[0].text
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    return {}
```

---

## Full Automation Script

```python
#!/usr/bin/env python3
# scripts/invoice_processor.py

import os
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
import smtplib
from email.mime.text import MIMEText

class InvoiceProcessor:
    def __init__(self, data_dir: str = "./invoice_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.invoices_file = self.data_dir / "invoices.json"
        self.load_invoices()
    
    def load_invoices(self):
        if self.invoices_file.exists():
            self.invoices = json.loads(self.invoices_file.read_text())
        else:
            self.invoices = []
    
    def save_invoices(self):
        self.invoices_file.write_text(json.dumps(self.invoices, indent=2, ensure_ascii=False))
    
    def process_invoice_pdf(self, pdf_path: str) -> dict:
        """Extract and process a single invoice PDF"""
        print(f"Processing: {pdf_path}")
        
        # Try Claude first, fallback to Tesseract
        try:
            data = extract_invoice_data_claude(pdf_path)
        except Exception as e:
            print(f"  Claude failed: {e}, trying OCR...")
            text = extract_invoice_data_ocr(pdf_path)
            data = self.parse_ocr_text(text)
        
        # Add metadata
        data["file_path"] = str(pdf_path)
        data["processed_at"] = datetime.now().isoformat()
        data["status"] = "pending_approval"
        data["id"] = f"INV-{len(self.invoices)+1:04d}"
        
        self.invoices.append(data)
        self.save_invoices()
        
        print(f"  ✅ Extracted: {data.get('vendor_name')} | Total: {data.get('total')} {data.get('currency')}")
        return data
    
    def parse_ocr_text(self, text: str) -> dict:
        """Basic regex parsing for common Indonesian invoice formats"""
        import re
        
        result = {}
        
        # Invoice number
        inv_match = re.search(r'(?:No\.?|Nomor|Invoice)[:\s#]*([A-Z0-9\-/]+)', text, re.I)
        if inv_match:
            result["invoice_number"] = inv_match.group(1)
        
        # Total
        total_match = re.search(r'(?:Total|Jumlah)[:\s]*(?:Rp\.?|IDR)?\s*([\d.,]+)', text, re.I)
        if total_match:
            total_str = total_match.group(1).replace(".", "").replace(",", "")
            result["total"] = int(total_str)
            result["currency"] = "IDR"
        
        # Date
        date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text)
        if date_match:
            result["invoice_date"] = date_match.group(1)
        
        return result
    
    def process_inbox(self, inbox_dir: str = "./invoices_inbox"):
        """Process all PDFs in inbox directory"""
        inbox = Path(inbox_dir)
        inbox.mkdir(exist_ok=True)
        
        pdfs = list(inbox.glob("*.pdf"))
        print(f"Found {len(pdfs)} invoices to process")
        
        processed = []
        for pdf in pdfs:
            try:
                data = self.process_invoice_pdf(str(pdf))
                processed.append(data)
                # Move to processed
                pdf.rename(self.data_dir / "processed" / pdf.name)
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        return processed
    
    def check_payment_reminders(self) -> list:
        """Check which invoices need payment reminders (outgoing — receivables)"""
        overdue = []
        due_soon = []
        today = datetime.now().date()
        
        for inv in self.invoices:
            if inv.get("type") != "receivable":
                continue
            if inv.get("status") in ("paid", "cancelled"):
                continue
            
            due_str = inv.get("due_date", "")
            if not due_str:
                continue
            
            try:
                due_date = datetime.fromisoformat(due_str).date()
            except:
                continue
            
            days_until = (due_date - today).days
            
            if days_until < 0:
                inv["days_overdue"] = abs(days_until)
                overdue.append(inv)
            elif days_until <= 3:
                inv["days_until_due"] = days_until
                due_soon.append(inv)
        
        return {"overdue": overdue, "due_soon": due_soon}
    
    def send_payment_reminder(self, invoice: dict, smtp_config: dict):
        """Send payment reminder email"""
        is_overdue = invoice.get("days_overdue") is not None
        days = invoice.get("days_overdue", invoice.get("days_until_due", 0))
        
        if is_overdue:
            subject = f"⚠️ OVERDUE: Invoice {invoice['invoice_number']} - {days} hari terlambat"
            body = f"""Yth. {invoice.get('customer_name', 'Pelanggan')},

Kami mengingatkan bahwa Invoice nomor {invoice['invoice_number']} 
dengan total {invoice.get('currency', 'IDR')} {invoice.get('total', 0):,}
sudah MELEWATI jatuh tempo {days} hari lalu.

Mohon segera lakukan pembayaran ke:
{invoice.get('bank_account', '[Rekening Perusahaan]')}

Jika sudah bayar, abaikan pesan ini.

Terima kasih,
{smtp_config.get('company_name', 'Tim Finance')}"""
        else:
            subject = f"Reminder: Invoice {invoice['invoice_number']} jatuh tempo {days} hari lagi"
            body = f"""Yth. {invoice.get('customer_name', 'Pelanggan')},

Mengingatkan bahwa Invoice {invoice['invoice_number']} 
sebesar {invoice.get('currency', 'IDR')} {invoice.get('total', 0):,}
akan jatuh tempo dalam {days} hari.

Rekening pembayaran:
{invoice.get('bank_account', '[Rekening Perusahaan]')}

Terima kasih atas kerja samanya!

{smtp_config.get('company_name', 'Tim Finance')}"""
        
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = smtp_config["email"]
        msg["To"] = invoice.get("customer_email", "")
        
        with smtplib.SMTP_SSL(smtp_config["smtp_host"], smtp_config["smtp_port"]) as server:
            server.login(smtp_config["email"], smtp_config["password"])
            server.sendmail(smtp_config["email"], [invoice["customer_email"]], msg.as_string())
        
        print(f"  ✅ Reminder sent to {invoice.get('customer_email')}")
    
    def export_csv(self, output_path: str = "./invoices_export.csv"):
        """Export all invoices to CSV for accounting software"""
        if not self.invoices:
            print("No invoices to export")
            return
        
        fieldnames = ["id", "vendor_name", "invoice_number", "invoice_date", 
                      "due_date", "total", "currency", "status", "processed_at"]
        
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(self.invoices)
        
        print(f"✅ Exported {len(self.invoices)} invoices to {output_path}")
    
    def generate_report(self) -> str:
        """Generate summary report"""
        total_amount = sum(inv.get("total", 0) for inv in self.invoices)
        pending = sum(1 for inv in self.invoices if inv.get("status") == "pending_approval")
        paid = sum(1 for inv in self.invoices if inv.get("status") == "paid")
        
        reminders = self.check_payment_reminders()
        
        report = f"""
📊 Invoice Report — {datetime.now().strftime('%Y-%m-%d')}

Total Invoices: {len(self.invoices)}
Total Amount: IDR {total_amount:,.0f}
Pending Approval: {pending}
Paid: {paid}

Payment Reminders Needed:
- Overdue: {len(reminders['overdue'])} invoices
- Due Soon (≤3 days): {len(reminders['due_soon'])} invoices
"""
        return report

if __name__ == "__main__":
    import sys
    processor = InvoiceProcessor()
    
    if "--inbox" in sys.argv:
        processor.process_inbox()
    elif "--reminders" in sys.argv:
        reminders = processor.check_payment_reminders()
        print(f"Overdue: {len(reminders['overdue'])}")
        print(f"Due soon: {len(reminders['due_soon'])}")
    elif "--report" in sys.argv:
        print(processor.generate_report())
    elif "--export" in sys.argv:
        processor.export_csv()
    else:
        print(processor.generate_report())
```

---

## Email Monitoring (Auto-ingest invoices from Gmail)

```python
# scripts/email_invoice_monitor.py
# Uses imap-smtp-email skill pattern

import imaplib
import email
from email.header import decode_header
import os
from pathlib import Path

def fetch_invoice_attachments(imap_config: dict, download_dir: str = "./invoices_inbox"):
    """Download PDF attachments from finance email"""
    Path(download_dir).mkdir(exist_ok=True)
    
    mail = imaplib.IMAP4_SSL(imap_config["host"])
    mail.login(imap_config["email"], imap_config["password"])
    mail.select("INBOX")
    
    # Search for unread emails with PDF attachments
    _, msgs = mail.search(None, '(UNSEEN)')
    msg_ids = msgs[0].split()
    
    downloaded = []
    for msg_id in msg_ids:
        _, msg_data = mail.fetch(msg_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        
        # Check for keywords indicating invoice
        invoice_keywords = ["invoice", "faktur", "tagihan", "nota", "receipt"]
        if not any(kw in subject.lower() for kw in invoice_keywords):
            continue
        
        for part in msg.walk():
            if part.get_content_type() == "application/pdf":
                filename = part.get_filename()
                if filename:
                    filepath = Path(download_dir) / filename
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    downloaded.append(str(filepath))
                    print(f"Downloaded: {filename}")
        
        # Mark as read
        mail.store(msg_id, "+FLAGS", "\\Seen")
    
    mail.logout()
    return downloaded
```

---

## Integration Points

- `imap-smtp-email` → Monitor email for incoming invoices
- `wa-business-automation` → Send payment reminders via WhatsApp
- `n8n` → Orchestrate full automation workflow
- `finance/finance-tracker` → Sync with existing tracker

---

## Client Pricing

| Package | Price/Month | What's Included |
|---------|-------------|-----------------|
| Basic | IDR 2M | OCR extraction, CSV export, manual reminders |
| Standard | IDR 5M | Auto email ingestion, auto reminders, accounting sync |
| Premium | IDR 10M | Full automation, multi-company, Accurate/Jurnal API |

**Setup fee**: 2x monthly rate

---

## Installation

```bash
pip install pytesseract pdf2image pillow anthropic

# Tesseract (Ubuntu/Kali)
sudo apt install tesseract-ocr tesseract-ocr-ind

# Run
python3 skills/invoice-automation/scripts/invoice_processor.py --inbox
python3 skills/invoice-automation/scripts/invoice_processor.py --reminders
python3 skills/invoice-automation/scripts/invoice_processor.py --report
```
