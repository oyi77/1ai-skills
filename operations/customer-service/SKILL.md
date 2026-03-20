---
name: customer-service
description: >
  Unified AI customer service — routes inquiries from WhatsApp + Telegram.
  Auto-response via OmniRoute LLM with template matching for BerkahKarya FAQs.
  Escalation to human review when confidence < 0.7.
version: "1.0.0"
author: BerkahKarya AI
tags: [customer-service, whatsapp, telegram, ai-response, berkahkarya, escalation]
---

# Multi-Channel AI Customer Service

## Overview

Unified customer service router handling inquiries from WhatsApp and Telegram. Uses template matching for common BerkahKarya questions and OmniRoute LLM for complex queries. Low-confidence responses are flagged for human review.

## Features

- **Template matching** for common questions (product info, pricing, shipping, returns)
- **LLM fallback** via OmniRoute for complex/novel questions
- **Confidence scoring** — escalates to human when confidence < 0.7
- **Multi-channel** — WhatsApp and Telegram unified interface
- **Interaction logging** to `logs/customer_service.log`

## Usage

```bash
# Process a customer message
python3 scripts/customer_service_router.py handle --channel telegram --message "berapa harga paket premium?"

# List template responses
python3 scripts/customer_service_router.py templates

# View escalation queue
python3 scripts/customer_service_router.py escalations
```

## Configuration

- **LLM**: OmniRoute at `http://localhost:20128/v1` (api_key: `omniroute`)
- **Confidence threshold**: 0.7 (configurable)
- **Log file**: `logs/customer_service.log`

## Template Categories

| Category | Triggers |
|----------|----------|
| Product Info | harga, produk, fitur, paket |
| Pricing | harga, biaya, diskon, promo |
| Shipping | kirim, ongkir, estimasi, pengiriman |
| Returns | retur, refund, garansi, tukar |
| General | jam operasional, kontak, alamat |
