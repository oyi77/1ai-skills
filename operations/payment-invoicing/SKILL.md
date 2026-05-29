---
name: payment-invoicing
description: Process payments and generate invoices using Indonesian payment gateways (TriPay, LYNK.ID, Midtrans). Create payment links, track transactions, and automate invoicing for 1-man company revenue collection.
---
persona:
  name: "Domain Expert"
  title: "Master of Payment Invoicing"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Payment & Invoicing Skill

## World-Class Expert Personas

This skill channels the expertise of:

### **Patrick Collison** - Stripe Co-Founder & Payments Visionary
- **Credentials**: Built Stripe to $95B valuation; processes $640B annually; revolutionized online payments
- **Expertise**: Payment infrastructure, API design, developer experience, global payment methods, fraud prevention
- **Philosophy**: "Make it as easy as possible for developers to accept payments."
- **Principles**: Developer-first design, transparent pricing, instant activation, comprehensive documentation, global scalability

### **Jack Dorsey** - Square Founder & Financial Inclusion Pioneer
- **Credentials**: Created Square ($40B company); democratized payment acceptance for small businesses
- **Expertise**: Point-of-sale systems, mobile payments, small business finance, payment hardware, cash flow management
- **Philosophy**: "Make commerce easy for everyone."
- **Principles**: Simplicity first, transparent fees, instant settlement, hardware + software integration, financial inclusion

### **Indonesian Fintech Experts** - Local Payment Ecosystem
- **Credentials**: Built GoPay, OVO, DANA (100M+ users); understand Indonesian payment behavior and regulations
- **Expertise**: Virtual accounts, QRIS, e-wallets, bank transfers, regulatory compliance (BI, OJK)
- **Philosophy**: "Cash is still king in Indonesia, but digital is the future."
- **Principles**: Multiple payment methods, instant confirmation, local bank integration, mobile-first, regulatory compliance

## Overview

Complete payment processing and invoicing solution for Indonesian businesses. Integrate with TriPay, LYNK.ID, and Midtrans to accept payments via Virtual Accounts, QRIS, E-Wallets, and more. Generate professional invoices, track payments, and automate revenue collection, applying world-class payment infrastructure principles.

**Supported Payment Gateways**:
- **TriPay** - Virtual Accounts, QRIS, E-Wallets, E-Banking
- **LYNK.ID** - Payment links, digital product sales
- **Midtrans** - Credit cards, QRIS, comprehensive payment methods

## When to Use

- Accept payments from customers
- Generate and send invoices
- Create payment links
- Track payment status
- Automate payment reminders
- Process subscriptions/recurring payments
- Handle refunds
- Generate payment reports

## When NOT to Use

- International payments only (use Stripe/PayPal)
- Complex accounting (use dedicated accounting software)
- POS systems (use dedicated POS solutions)

---

## Indonesian Payment Gateway Comparison

| Feature | TriPay | LYNK.ID | Midtrans |
|---------|--------|---------|----------|
| **Virtual Accounts** | ✅ Yes | ❌ No | ✅ Yes |
| **QRIS** | ✅ Yes | ❌ No | ✅ Yes |
| **E-Wallets** | ✅ Yes (OVO, DANA, etc) | ✅ Yes | ✅ Yes |
| **Credit Cards** | ❌ No | ❌ No | ✅ Yes |
| **Payment Links** | ✅ Yes | ✅ Yes (Primary) | ✅ Yes |
| **API Integration** | ✅ Full API | ⚠️ Webhook only | ✅ Full API |
| **Best For** | Virtual Accounts | Simple payment links | Comprehensive solutions |
| **Pricing** | Low fees | Low fees | Competitive |

---

## TriPay Integration

Payment gateway integration with TriPay for Indonesian merchants.


### Overview
TriPay offers Direct and Redirect integration with various Indonesian payment methods.

**Payment Methods**:
- Virtual Accounts (BCA, BNI, Mandiri, BRI, etc.)
- QRIS (Indonesia's QR payment standard)
- Convenience Stores (Indomaret, Alfamart)
- E-Wallets (OVO, DANA, ShopeePay, LinkAja)
- E-Banking

### Setup

**Step 1: Get API Credentials**
```
1. Register at https://tripay.co.id
2. Navigate to Settings → API
3. Get your:
   - Merchant Code
   - API Key
   - Private Key
4. Test in Sandbox first
```

**Step 2: Generate Authorization Token**
```javascript
// TriPay uses HMAC-SHA256 for authentication
const crypto = require('crypto');

function generateTriPaySignature(merchantCode, apiKey, privateKey) {
  const data = merchantCode + apiKey;
  const signature = crypto
    .createHmac('sha256', privateKey)
    .update(data)
    .digest('hex');
  
  return signature;
}
```

### Create Payment (Closed Payment)

**Step 1: Request Transaction**
```javascript
const axios = require('axios');

async function createTriPayPayment(orderData) {
  const merchantCode = 'YOUR_MERCHANT_CODE';
  const apiKey = 'YOUR_API_KEY';
  const privateKey = 'YOUR_PRIVATE_KEY';
  
  const signature = generateTriPaySignature(merchantCode, apiKey, privateKey);
  
  const payload = {
    method: 'BRIVA',  // Payment channel (BRI Virtual Account)
    merchant_ref: `INV-${Date.now()}`,
    amount: orderData.amount,
    customer_name: orderData.customerName,
    customer_email: orderData.customerEmail,
    customer_phone: orderData.customerPhone,
    order_items: orderData.items,
    return_url: 'https://yoursite.com/payment/return',
    expired_time: Math.floor(Date.now() / 1000) + (24 * 60 * 60), // 24 hours
    signature: signature
  };
  
  const response = await axios.post(
    'https://tripay.co.id/api/transaction/create',
    payload,
    {
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    }
  );
  
  return response.data;
}

// Usage
const payment = await createTriPayPayment({
  amount: 100000,  // IDR 100,000
  customerName: 'John Doe',
  customerEmail: 'john@example.com',
  customerPhone: '081234567890',
  items: [
    {
      name: 'AI Video Generation Service',
      price: 100000,
      quantity: 1
    }
  ]
});

console.log('Payment Code:', payment.data.pay_code);
console.log('Payment URL:', payment.data.checkout_url);
```

### Check Payment Status

```javascript
async function checkTriPayStatus(reference) {
  const response = await axios.get(
    `https://tripay.co.id/api/transaction/detail?reference=${reference}`,
    {
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    }
  );
  
  return response.data.data.status;
  // Status: UNPAID, PAID, EXPIRED, FAILED
}
```

### Handle Webhook (Payment Notification)

```javascript
const express = require('express');
const app = express();

app.post('/webhook/tripay', express.json(), (req, res) => {
  const callbackSignature = req.headers['x-callback-signature'];
  const payload = req.body;
  
  // Verify signature
  const calculatedSignature = crypto
    .createHmac('sha256', privateKey)
    .update(JSON.stringify(payload))
    .digest('hex');
  
  if (callbackSignature !== calculatedSignature) {
    return res.status(400).send('Invalid signature');
  }
  
  // Process payment
  if (payload.status === 'PAID') {
    console.log('Payment received:', payload.reference);
    // Update order status, send confirmation email, etc.
  }
  
  res.status(200).send('OK');
});
```

---

## LYNK.ID Integration

Digital payment integration with LYNK.ID.


### Overview
LYNK.ID is a "link in bio" platform with payment link functionality. Best for simple payment collection and digital product sales.

### Setup

**Step 1: Create Account**
```
1. Register at https://lynk.id
2. Complete profile
3. Connect bank account for withdrawals
```

**Step 2: Create Payment Link**
```
1. Navigate to "Produk" or "Link Pembayaran"
2. Click "Buat Produk Baru"
3. Fill in:
   - Product name
   - Price
   - Description
   - Image (optional)
4. Get payment link
```

### Webhook Integration

**Step 1: Get Webhook URL**
```
1. Go to Settings → Webhook
2. Get your Merchant Key
3. Set webhook URL: https://yoursite.com/webhook/lynk
```

**Step 2: Handle Webhook**
```javascript
app.post('/webhook/lynk', express.json(), (req, res) => {
  const { merchant_key, order_id, status, amount, customer_email } = req.body;
  
  // Verify merchant key
  if (merchant_key !== process.env.LYNK_MERCHANT_KEY) {
    return res.status(400).send('Invalid merchant key');
  }
  
  // Process payment
  if (status === 'paid') {
    console.log(`Payment received: ${amount} for order ${order_id}`);
    // Send product, update database, etc.
  }
  
  res.status(200).send('OK');
});
```

### Automated Payment Link Creation

```javascript
// Note: LYNK.ID doesn't have public API for link creation
// Use browser automation instead

async function createLynkPaymentLink(productData) {
  // 1. Navigate to https://lynk.id/dashboard
  // 2. Click "Buat Produk"
  // 3. Fill form:
  //    - Name: productData.name
  //    - Price: productData.price
  //    - Description: productData.description
  // 4. Click "Simpan"
  // 5. Copy generated link
  
  return {
    link: 'https://lynk.id/username/product-slug',
    productId: 'generated-id'
  };
}
```

---

## Midtrans Integration

Midtrans payment gateway integration for cards, bank transfers, and e-wallets.


### Overview
Midtrans is Indonesia's most comprehensive payment gateway with full API support.

**APIs Available**:
- **Snap API** - Built-in checkout page
- **Core API** - Custom payment interface
- **Iris API** - Disbursement/payout

### Setup

**Step 1: Get API Credentials**
```
1. Register at https://midtrans.com
2. Navigate to Settings → Access Keys
3. Get your:
   - Server Key
   - Client Key
4. Use Sandbox for testing
```

**Step 2: Install SDK**
```bash
npm install midtrans-client
```

### Create Payment (Snap API)

```javascript
const midtransClient = require('midtrans-client');

// Initialize Snap API
const snap = new midtransClient.Snap({
  isProduction: false,  // Use true for production
  serverKey: 'YOUR_SERVER_KEY'
});

async function createMidtransPayment(orderData) {
  const parameter = {
    transaction_details: {
      order_id: `ORDER-${Date.now()}`,
      gross_amount: orderData.amount
    },
    credit_card: {
      secure: true
    },
    customer_details: {
      first_name: orderData.customerName,
      email: orderData.customerEmail,
      phone: orderData.customerPhone
    },
    item_details: orderData.items,
    callbacks: {
      finish: 'https://yoursite.com/payment/finish',
      error: 'https://yoursite.com/payment/error',
      pending: 'https://yoursite.com/payment/pending'
    }
  };
  
  const transaction = await snap.createTransaction(parameter);
  
  return {
    token: transaction.token,
    redirect_url: transaction.redirect_url
  };
}

// Usage
const payment = await createMidtransPayment({
  amount: 150000,  // IDR 150,000
  customerName: 'Jane Doe',
  customerEmail: 'jane@example.com',
  customerPhone: '081234567890',
  items: [
    {
      id: 'ITEM1',
      price: 150000,
      quantity: 1,
      name: 'Premium Video Package'
    }
  ]
});

console.log('Payment URL:', payment.redirect_url);
```

### Check Payment Status

```javascript
const core = new midtransClient.CoreApi({
  isProduction: false,
  serverKey: 'YOUR_SERVER_KEY'
});

async function checkMidtransStatus(orderId) {
  const status = await core.transaction.status(orderId);
  
  return {
    status: status.transaction_status,
    // Status: capture, settlement, pending, deny, cancel, expire
    paymentType: status.payment_type,
    amount: status.gross_amount
  };
}
```

### Handle Webhook

```javascript
app.post('/webhook/midtrans', express.json(), (req, res) => {
  const notification = req.body;
  const orderId = notification.order_id;
  const transactionStatus = notification.transaction_status;
  const fraudStatus = notification.fraud_status;
  
  // Verify signature
  const crypto = require('crypto');
  const serverKey = process.env.MIDTRANS_SERVER_KEY;
  const hash = crypto.createHash('sha512')
    .update(orderId + notification.status_code + notification.gross_amount + serverKey)
    .digest('hex');
  
  if (hash !== notification.signature_key) {
    return res.status(400).send('Invalid signature');
  }
  
  // Process based on status
  if (transactionStatus === 'capture' || transactionStatus === 'settlement') {
    if (fraudStatus === 'accept') {
      console.log('Payment successful:', orderId);
      // Fulfill order
    }
  } else if (transactionStatus === 'cancel' || transactionStatus === 'deny' || transactionStatus === 'expire') {
    console.log('Payment failed:', orderId);
    // Cancel order
  } else if (transactionStatus === 'pending') {
    console.log('Payment pending:', orderId);
    // Wait for payment
  }
  
  res.status(200).send('OK');
});
```

---

## Invoice Generation

Automated invoice creation with tax calculations and payment terms.


### Create Professional Invoice

```javascript
const PDFDocument = require('pdfkit');
const fs = require('fs');

function generateInvoice(invoiceData) {
  const doc = new PDFDocument();
  const filename = `invoice-${invoiceData.invoiceNumber}.pdf`;
  
  doc.pipe(fs.createWriteStream(filename));
  
  // Header
  doc.fontSize(20).text('INVOICE', { align: 'center' });
  doc.moveDown();
  
  // Company info
  doc.fontSize(12).text('Your Company Name');
  doc.fontSize(10).text('Address Line 1');
  doc.text('Address Line 2');
  doc.text('Phone: +62 xxx xxxx xxxx');
  doc.text('Email: info@yourcompany.com');
  doc.moveDown();
  
  // Invoice details
  doc.text(`Invoice Number: ${invoiceData.invoiceNumber}`);
  doc.text(`Date: ${new Date().toLocaleDateString('id-ID')}`);
  doc.text(`Due Date: ${invoiceData.dueDate}`);
  doc.moveDown();
  
  // Bill to
  doc.text('Bill To:');
  doc.text(invoiceData.customerName);
  doc.text(invoiceData.customerEmail);
  doc.text(invoiceData.customerPhone);
  doc.moveDown();
  
  // Items table
  doc.text('Description                    Qty    Price         Total');
  doc.text('─'.repeat(60));
  
  let subtotal = 0;
  invoiceData.items.forEach(item => {
    const total = item.quantity * item.price;
    subtotal += total;
    doc.text(
      `${item.name.padEnd(30)} ${item.quantity.toString().padEnd(6)} ${item.price.toLocaleString('id-ID').padEnd(13)} ${total.toLocaleString('id-ID')}`
    );
  });
  
  doc.text('─'.repeat(60));
  doc.moveDown();
  
  // Totals
  const tax = subtotal * 0.11; // 11% PPN (Indonesian VAT)
  const total = subtotal + tax;
  
  doc.text(`Subtotal: Rp ${subtotal.toLocaleString('id-ID')}`, { align: 'right' });
  doc.text(`PPN (11%): Rp ${tax.toLocaleString('id-ID')}`, { align: 'right' });
  doc.fontSize(14).text(`Total: Rp ${total.toLocaleString('id-ID')}`, { align: 'right' });
  
  doc.moveDown();
  
  // Payment instructions
  doc.fontSize(10).text('Payment Instructions:');
  doc.text(`Please pay via: ${invoiceData.paymentMethod}`);
  doc.text(`Payment Link: ${invoiceData.paymentLink}`);
  
  doc.end();
  
  return filename;
}

// Usage
const invoice = generateInvoice({
  invoiceNumber: 'INV-2026-001',
  dueDate: '2026-02-24',
  customerName: 'John Doe',
  customerEmail: 'john@example.com',
  customerPhone: '081234567890',
  items: [
    { name: 'AI Video Generation', quantity: 1, price: 100000 },
    { name: 'Social Media Upload', quantity: 1, price: 50000 }
  ],
  paymentMethod: 'TriPay Virtual Account',
  paymentLink: 'https://tripay.co.id/checkout/xxx'
});
```

---

## Complete Payment Workflow

End-to-end payment flow from invoice creation to reconciliation.


### End-to-End Example

```javascript
async function processCustomerOrder(orderData) {
  // 1. Generate invoice
  const invoiceNumber = `INV-${Date.now()}`;
  const invoiceFile = generateInvoice({
    ...orderData,
    invoiceNumber
  });
  
  // 2. Create payment (choose gateway)
  let payment;
  if (orderData.preferredGateway === 'tripay') {
    payment = await createTriPayPayment(orderData);
  } else if (orderData.preferredGateway === 'midtrans') {
    payment = await createMidtransPayment(orderData);
  }
  
  // 3. Send invoice email
  await sendInvoiceEmail({
    to: orderData.customerEmail,
    subject: `Invoice ${invoiceNumber}`,
    body: `
      Dear ${orderData.customerName},
      
      Thank you for your order!
      
      Please find your invoice attached.
      
      Payment Link: ${payment.redirect_url || payment.data.checkout_url}
      
      Amount: Rp ${orderData.amount.toLocaleString('id-ID')}
      
      Best regards,
      Your Company
    `,
    attachments: [invoiceFile]
  });
  
  // 4. Track payment status
  const paymentId = payment.data?.reference || payment.token;
  
  return {
    invoiceNumber,
    paymentId,
    paymentUrl: payment.redirect_url || payment.data.checkout_url,
    status: 'pending'
  };
}
```

---

## Best Practices

Key aspects of payment-invoicing relevant to this section.


### 1. Security
- Never expose private keys in frontend
- Verify webhook signatures
- Use HTTPS for all endpoints
- Store credentials in environment variables

### 2. User Experience
- Clear payment instructions
- Multiple payment options
- Mobile-friendly payment pages
- Instant payment confirmation

### 3. Automation
- Auto-send invoices
- Payment reminders (24h before due)
- Receipt generation on payment
- Failed payment notifications

### 4. Tracking
- Log all transactions
- Monitor payment success rate
- Track payment method preferences
- Generate revenue reports

---


## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Operational changes are made without stakeholder communication
- Agent does not track compliance with established processes
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Changes are communicated to stakeholders before implementation
- [ ] Compliance with established processes is tracked and reported
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- `marketing/email-marketing` - Send invoices and reminders
- sales/crm-automation - Track customer payments
- `marketing/analytics-dashboard` - Revenue analytics
- `automation/workflow-builder` - Automate payment workflows

---

**Last Updated**: 2026-02-17  
**Payment Gateways**: TriPay, LYNK.ID, Midtrans  
**Region**: Indonesia  
**Key Feature**: Multi-gateway support with automated invoicing
