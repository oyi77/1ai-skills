---
name: email-marketing
description: Create and send email campaigns, newsletters, and drip sequences. Build email lists, design templates, automate follow-ups, and track email performance for customer nurturing.
---

# Email Marketing Skill

## Overview

Complete email marketing automation for customer nurturing. Create campaigns, send newsletters, build drip sequences, and track performance. Essential for 1-man company lead nurturing and customer retention.

## When to Use

- Send newsletters
- Nurture leads with drip campaigns
- Announce new products/services
- Send invoices and receipts
- Follow up with customers
- Automate welcome sequences
- Re-engage inactive customers

## Email Service Providers

### Recommended for Indonesia
1. **Mailchimp** - Free tier, easy to use
2. **SendGrid** - Developer-friendly, good deliverability
3. **KIRIM.EMAIL** - Indonesian service, local support

## Campaign Types

### 1. Newsletter
```javascript
const newsletter = {
  subject: '🎥 This Week in AI Video',
  to: 'subscribers@list',
  content: `
    Hi {first_name},
    
    Check out this week's highlights:
    
    1. New AI video feature released
    2. Tutorial: Creating viral TikTok videos
    3. Case study: 100K views in 24 hours
    
    [Read More]
    
    Best,
    Your Name
  `,
  schedule: 'Every Monday 10:00 AM'
};
```

### 2. Drip Campaign (Welcome Sequence)
```javascript
const welcomeSequence = [
  {
    day: 0,
    subject: 'Welcome! Here\'s what to expect',
    content: 'Thanks for subscribing...'
  },
  {
    day: 2,
    subject: 'Quick tip: Your first AI video',
    content: 'Let me show you how...'
  },
  {
    day: 5,
    subject: 'Special offer for new subscribers',
    content: '20% off your first order...'
  },
  {
    day: 10,
    subject: 'How are you finding our service?',
    content: 'I\'d love your feedback...'
  }
];
```

### 3. Transactional Emails
```javascript
// Invoice email
const invoiceEmail = {
  to: customer.email,
  subject: `Invoice ${invoiceNumber}`,
  template: 'invoice',
  data: {
    invoiceNumber,
    amount,
    dueDate,
    paymentLink
  }
};

// Receipt email
const receiptEmail = {
  to: customer.email,
  subject: 'Payment Received - Thank You!',
  template: 'receipt',
  data: {
    orderNumber,
    amount,
    items
  }
};
```

## Email Templates

### Basic Template Structure
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; }
    .container { max-width: 600px; margin: 0 auto; }
    .header { background: #4F46E5; color: white; padding: 20px; }
    .content { padding: 20px; }
    .button { background: #4F46E5; color: white; padding: 12px 24px; text-decoration: none; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Your Company Name</h1>
    </div>
    <div class="content">
      {{content}}
      <br><br>
      <a href="{{cta_link}}" class="button">{{cta_text}}</a>
    </div>
  </div>
</body>
</html>
```

## Automation Examples

### SendGrid Integration
```javascript
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

async function sendEmail(emailData) {
  const msg = {
    to: emailData.to,
    from: 'your@email.com',
    subject: emailData.subject,
    text: emailData.text,
    html: emailData.html
  };
  
  await sgMail.send(msg);
}
```

### Automated Invoice Sending
```javascript
async function sendInvoiceEmail(invoice) {
  await sendEmail({
    to: invoice.customerEmail,
    subject: `Invoice ${invoice.number}`,
    html: `
      <h2>Invoice ${invoice.number}</h2>
      <p>Amount: Rp ${invoice.amount.toLocaleString('id-ID')}</p>
      <p>Due: ${invoice.dueDate}</p>
      <a href="${invoice.paymentLink}">Pay Now</a>
    `
  });
}
```

## List Management

### Segmentation
```javascript
const segments = {
  new_subscribers: 'Joined < 30 days',
  active_customers: 'Purchased in last 90 days',
  inactive: 'No activity > 90 days',
  high_value: 'LTV > Rp 1,000,000'
};
```

### Personalization
```javascript
const personalizedEmail = {
  subject: 'Hi {{first_name}}, check this out!',
  content: `
    Hi {{first_name}},
    
    Based on your interest in {{interest}}, 
    I thought you'd like this...
  `
};
```

## Best Practices

1. **Subject Lines**
   - Keep under 50 characters
   - Use emojis sparingly
   - Create urgency/curiosity
   - Personalize when possible

2. **Content**
   - Mobile-friendly design
   - Clear call-to-action
   - Short paragraphs
   - Valuable content first

3. **Timing**
   - Test different send times
   - Avoid weekends (B2B)
   - Consider timezone

4. **Compliance**
   - Include unsubscribe link
   - Add physical address
   - Get consent (GDPR/local laws)
   - Honor opt-outs immediately

---

**Related Skills**: `operations/payment-invoicing`, `marketing/content-creator`, `sales/crm-automation`
