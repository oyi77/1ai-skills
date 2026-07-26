---
name: email-writer
description: Use when writing email copy — sales sequences, newsletters, onboarding flows with subject line strategy, preview text, and progressive story arcs.
domain: content
tags: [content-creation, email]
version: 1.0.0
---

# Email Writer

Quick Reference — for full workflow see [../SKILL.md](../SKILL.md).

Email remains the highest-ROI channel at 4,200%. This sub-skill covers the 5-email progression (welcome → nurture → social proof → objections → close) with subject line and preview text strategy designed to move recipients from cold to conversion.

## Quick Start

1. **Define sequence goal** — Single CTA per sequence (launch, reactivation, upsell). Map the arc: open → read → click → convert.
2. **Draft 5-stage progression** — Use `generate_email_sequence()` for welcome, value, social proof, FAQ-overcome, final push.
3. **Subject line audit** — Check each subject passes the "would I open this in a crowded inbox?" test. Add preview text that complements (not repeats) the subject.

## Key Function: 5-Email Sales Sequence

```python
def generate_email_sequence(
    product: str,
    audience: str,
    benefits: list[str],
    cta: str,
    sender_name: str = "Team",
) -> list[dict]:
    """
    Generate a 5-email sales sequence progressing through:
    welcome → nurture → social proof → overcome objections → final close
    """
    sequence = [
        {
            "subject": f"Quick question for {audience.lower()}",
            "preview": "I have a thought...",
            "body": f"Hey there,\n\nI noticed you're {audience.lower()}. I wanted to share something that's been helping people like you get {benefits[0].lower()}.\n\nMore tomorrow,\n{sender_name}",
        },
        {
            "subject": f"The {benefits[0]} problem (and how to fix it)",
            "preview": "Here's what most people miss...",
            "body": f"Hi again,\n\nMost {audience.lower()} struggle with {benefits[0].lower()}. They try everything but nothing sticks.\n\n{product} was built specifically for this. Let me show you how:\n\n" + "\n".join(f"• {b}" for b in benefits) + f"\n\nCheck it out: {cta}\n\n{sender_name}",
        },
        {
            "subject": f"Real results from {audience.lower()}",
            "preview": "See what others are saying...",
            "body": f"Hey,\n\nDon't take my word for it. Here's what other {audience.lower()} achieved with {product}:\n\n\"{benefits[0]} in just 2 weeks!\"\n\"Finally, a solution that works.\"\n\"Wish I found this sooner.\"\n\nYou could be next.\n\n{cta}\n\n{sender_name}",
        },
        {
            "subject": f"Still thinking about {benefits[0].lower()}?",
            "preview": "Let me address your concerns...",
            "body": f"Hi,\n\nIf you're still on the fence, here are the most common questions I get:\n\nQ: Does it really work?\nA: {benefits[0]} is exactly what {product} delivers, guaranteed.\n\nQ: Is it right for me?\nA: If you're {audience.lower()}, yes.\n\nQ: What if it doesn't work?\nA: You're covered. No risk.\n\nReady to decide? {cta}\n\n{sender_name}",
        },
        {
            "subject": f"Final chance — {benefits[0].lower()}",
            "preview": "This is your last email from me...",
            "body": f"Hey,\n\nI wanted to give you one last opportunity to try {product}.\n\n{benefits[0].lower()} is just a click away:\n\n{cta}\n\nIf now's not the right time, no hard feelings. I'll see you down the road.\n\nBest,\n{sender_name}",
        },
    ]
    return sequence

# Subject line rules: under 50 chars, no ALL CAPS, ask a question or state a benefit,
# personalize with audience name. Preview text should extend (not repeat) the subject.
```

## Verification Checklist

- [ ] 5 emails with clear progression arc (welcome → nurture → proof → objections → close)
- [ ] Subject lines ≤50 characters, unique across the sequence
- [ ] Preview text adds context (doesn't repeat the subject line)
- [ ] Single CTA per email, consistent across the sequence
- [ ] Sender name is a real person (not "noreply@..." or "Team Sales")
- [ ] Plain text format for initial sends (HTML triggers spam filters)
- [ ] Unsubscribe link present and RFC 2369 compliant

## Workflow

Execute these steps sequentially:

1. **Define sequence goal** — Single CTA per sequence (launch, reactivation, upsell). Map the arc: open → read → click → convert.
2. **Draft 5-stage progression** — Use `generate_email_sequence()` for welcome, value, social proof, FAQ-overcome, final push.
3. **Subject line audit** — Check each subject passes the "would I open this in a crowded inbox?" test. Add preview text that complements (not repeats) the subject.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Long emails convert better" | Short, scannable emails outperform long ones 2:1. Respect inbox attention span — 100-200 words max. |
| "Subject lines should summarize the email" | The best subject lines create curiosity gaps. The reader should need to open to resolve it. |
| "More emails = more sales" | 5 well-written emails beat 20 mediocre ones. Sequence length matters less than value per email. |
| "Everyone reads the whole email" | 80% of clicks happen above the fold. Put the CTA and the main value proposition before the scroll. |

## When to Use
Use this skill when writing email sequences for sales launches, onboarding flows, newsletter campaigns, reactivation drips, or any email funnel that needs a structured progression.
