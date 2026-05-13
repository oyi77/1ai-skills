# Execution Engine Reference

The skill doesn't just generate content — it REVIEWS it, then SENDS it.
AI drafts → AI self-reviews → AI executes. You focus on product.

---

## The Autonomous Execution Model

```
OLD (manual):  AI drafts → you review → you send    → hours wasted
NEW (auto):    AI drafts → AI reviews → AI sends     → you build product
```

### How Auto-Review Works

Every piece of content passes through an automated quality gate BEFORE
being sent or published. The gate checks against YOUR standards (from
marketing-profile.yml, brand-voice.md, and persona.md).

If it passes all checks → **auto-execute** (send email, create event, etc.)
If it fails any check → **flag for human review** with the specific issue

---

## The Quality Gate (Auto-Review Checklist)

Before any content is sent/published, run it through this checklist.
All items must PASS or the content is held for human review.

### Email Quality Gate (Cold Outreach, Follow-ups, Sequences)

```
MUST PASS ALL:
□ PERSONALIZATION: Contains specific detail about the recipient
  (not generic "I admire your company" — actual reference to their
  work, recent post, product, or situation)
  FAIL if: Opens with generic flattery or has no personalization

□ BRAND VOICE: Matches tone defined in brand-voice.md
  Check: formality level, personality adjectives, forbidden words
  FAIL if: Uses words on the "never use" list, wrong tone

□ VALUE PROPOSITION: Clear benefit in first 2 sentences
  FAIL if: Talks about yourself before addressing their problem

□ CTA: Single, specific, low-friction call to action
  FAIL if: No CTA, multiple CTAs, or high-friction ask (e.g., "buy now"
  in a first cold email)

□ LENGTH: Under 150 words for cold email, under 300 for follow-up
  FAIL if: Too long (cold emails over 150 words get ignored)

□ SPAM FILTER: No spam trigger words or patterns
  Check against: "FREE!!!", ALL CAPS, excessive punctuation,
  misleading subject lines, no unsubscribe for bulk
  FAIL if: Would trigger spam filters

□ RECIPIENT CHECK: Valid email, not a competitor, not already contacted
  in the last 14 days
  FAIL if: Duplicate outreach or invalid target

□ SUBJECT LINE: Under 50 chars, curiosity or relevance driven
  FAIL if: Generic ("Quick question"), clickbait, or over 60 chars

GATE RESULT:
  8/8 pass → AUTO-SEND via Gmail
  7/8 pass → AUTO-SEND with note about what was marginal
  <7 pass  → HOLD for human review (show what failed)
```

### Social Post Quality Gate

```
MUST PASS ALL:
□ PLATFORM FIT: Meets platform character limits and format norms
  (LinkedIn: professional tone, <3000 chars; Twitter: <280 chars;
  Instagram: visual-first, <2200 chars)

□ HOOK: First line is scroll-stopping (question, bold claim,
  specific number, or pattern interrupt)
  FAIL if: Starts with generic statement

□ BRAND VOICE: Matches brand-voice.md personality
  FAIL if: Off-brand tone or uses forbidden phrases

□ VALUE: Provides actionable insight, data, or story
  FAIL if: Pure self-promotion without value

□ CTA: Ends with engagement prompt (question, share, comment)
  or clear next step

□ NO SENSITIVE CONTENT: Nothing controversial, offensive,
  or potentially reputation-damaging

GATE RESULT:
  6/6 pass → AUTO-PUBLISH (or queue for optimal time)
  5/6 pass → AUTO-PUBLISH with adjustment note
  <5 pass  → HOLD for human review
```

### Ad Copy Quality Gate

```
MUST PASS ALL:
□ HOOK: First 3 words grab attention
□ PROBLEM-SOLUTION: Addresses specific pain → clear solution
□ PROOF: Contains social proof, number, or credibility signal
□ CTA: Clear, action-oriented, platform-appropriate
□ PLATFORM SPECS: Meets character limits, image requirements
□ BUDGET CHECK: Spend within daily/monthly limits

GATE RESULT:
  6/6 pass → LAUNCH via Adspirer
  <6 pass  → HOLD for human review
```

---

## Connected Tools (MCP Integration)

### Available Tools + Auto-Execute Actions

**Gmail (Connected — draft only)**
- `Gmail:create_draft` → create draft
- `Gmail:search_threads` → check for existing conversations before outreach
- `Gmail:get_thread` → read context for follow-up personalization
- NOTE: Gmail MCP only supports create_draft, not direct send.

**AUTO-SEND SOLUTIONS (Choose One):**

Option A — **MailerLite MCP (recommended for sequences/bulk)**
  Connect MailerLite from the MCP registry. It supports:
  `send_campaign`, `create_automation`, `add_subscriber`, and 37+ tools.
  This enables true auto-send for email sequences, newsletters, and
  bulk outreach — all triggered by the skill without manual clicking.
  Setup: Connect MailerLite MCP → import contacts → skill sends directly.

Option B — **Outreach MCP (for sales sequences)**
  Connect Outreach from MCP registry for automated sales sequences.
  Supports `sequence_search`, `prospect_search`, email tracking.
  Best for: multi-step cold outreach sequences with auto-follow-up.

Option C — **Gmail Draft + Google Apps Script Auto-Sender (DIY)**
  The skill creates drafts with a special label "[AUTO-SEND]".
  A Google Apps Script runs every 5 minutes and auto-sends all drafts
  with that label. Setup once, runs forever:
  
  ```javascript
  // Google Apps Script — runs on timer trigger every 5 minutes
  function autoSendLabeledDrafts() {
    var drafts = GmailApp.getDrafts();
    drafts.forEach(function(draft) {
      var message = draft.getMessage();
      var subject = message.getSubject();
      // Only send drafts that start with [AUTO-SEND]
      if (subject.startsWith('[AUTO-SEND]')) {
        // Remove the [AUTO-SEND] prefix before sending
        var cleanSubject = subject.replace('[AUTO-SEND] ', '');
        var to = message.getTo();
        var body = message.getPlainBody();
        var htmlBody = message.getBody();
        GmailApp.sendEmail(to, cleanSubject, body, {htmlBody: htmlBody});
        draft.deleteDraft();
      }
    });
  }
  // Set up: Google Apps Script > Triggers > autoSendLabeledDrafts > 
  // Time-driven > Minutes timer > Every 5 minutes
  ```
  
  With this script, the skill creates a draft with subject 
  "[AUTO-SEND] Quick question about your workflow" → Google Apps Script
  picks it up within 5 minutes → sends it → deletes the draft.
  Fully autonomous. You never touch Gmail.

Option D — **Gmail Draft + Zapier/Make Auto-Sender**
  Create a Zap/Make scenario: "When new Gmail draft with label 
  'auto-send' → Send the draft → Remove label"
  No coding required. Same result as Option C.

**Google Calendar (Connected)**
- **AUTO-CREATE:** Follow-up reminders, content publishing schedules,
  review meetings — all created automatically, no approval needed
- Schedule demo calls when prospect responds positively
- Block daily marketing time slots

**Adspirer (Connected)**
- **AUTO-MANAGE:** Pull performance data, pause underperforming ads,
  reallocate budget to winners — within pre-set rules
- Launch new ad variants that pass quality gate
- Generate performance reports

---

## Autonomous Execution Workflows

### Workflow 1: Auto-Outreach Pipeline (Runs Daily, Zero Intervention)

```
TRIGGER: Daily at start of work session OR "/marketing-ops daily"

STEP 1: PROSPECT (AI — automated)
  → Search web for potential leads matching ICP from persona.md
  → Search Gmail to verify no existing conversation with them
  → Check: not a competitor, not contacted in last 14 days
  → Output: 5 qualified prospects with personalization hooks

STEP 2: DRAFT (AI — automated)
  → Generate personalized cold email for each prospect
  → Use sales.md cold email framework
  → Personalize with: their recent activity, specific pain point, relevant CTA
  → Apply brand-voice.md tone and style

STEP 3: SELF-REVIEW (AI — automated quality gate)
  → Run each email through Email Quality Gate (8 checks)
  → Score: personalization ✓ voice ✓ value prop ✓ CTA ✓ length ✓
    spam check ✓ recipient ✓ subject ✓

STEP 4: EXECUTE (AI — automated)
  → PASSED (8/8): Create Gmail draft with subject prefix "[AUTO-SEND]"
    If auto-sender is configured (Apps Script/Zapier/Make), it sends
    automatically within 5 minutes. Zero human intervention.
  → PASSED (7/8): Create draft with "[AUTO-SEND]" + note in body footer
    about what was marginal
  → FAILED (<7): Create draft with "[NEEDS REVIEW]" prefix instead
    — this one stays as a draft until you manually review and send
  
STEP 5: FOLLOW-UP SCHEDULING (AI — automated)
  → Create Google Calendar reminders for Day 3, Day 7, Day 14
  → If prospect responds → AI drafts contextual reply → quality gate → execute
  → If no response Day 3 → AI drafts follow-up #2 → quality gate → execute
  → If no response Day 7 → AI drafts breakup email → quality gate → execute

DAILY OUTPUT (total time for you: 2 minutes to open Gmail and hit send on
pre-approved drafts):
  - 5 new outreach emails ready to send
  - Follow-up emails for previous contacts
  - All calendar reminders set
  - Pipeline tracking updated
```

### Workflow 2: Content Auto-Publish Pipeline

```
TRIGGER: Content calendar date OR "/marketing-ops content auto"

STEP 1: GENERATE (AI — automated)
  → Write blog post using content.md + seo.md + geo.md frameworks
  → Generate 5 social variants (LinkedIn, Twitter/X, Instagram)
  → Generate newsletter snippet

STEP 2: OPTIMIZE (AI — automated)
  → GEO: Quick Answer blocks, schema, FAQ
  → SEO: Title, meta, headers, keyword density
  → Social: Platform-specific formatting, hashtags, hooks

STEP 3: SELF-REVIEW (AI — automated quality gate)
  → Blog: brand voice ✓ SEO score ✓ readability ✓ CTA ✓ length ✓
  → Social: platform fit ✓ hook ✓ voice ✓ value ✓ CTA ✓
  → Newsletter: subject line ✓ preview text ✓ body ✓

STEP 4: EXECUTE (AI — automated)
  → Blog: Save to marketing-outputs/ with "publish-ready" flag
  → Social: Queue for posting (save with platform + scheduled time)
  → Newsletter: Create Gmail draft to subscriber list
  → Calendar: Create publishing reminder events

YOUR ROLE: Copy-paste blog to CMS (1 min), copy-paste social posts (2 min).
Everything else is pre-reviewed and pre-formatted.
```

### Workflow 3: Response Triage + Auto-Reply

```
TRIGGER: "/marketing-ops triage" OR daily morning check

STEP 1: SCAN (AI — automated)
  → Search Gmail for new responses to outreach
  → Search for inbound inquiries
  → Categorize each: HOT (interested) / WARM (questions) / COLD (not now)

STEP 2: AUTO-RESPOND (AI — automated per category)
  
  HOT (expressed interest):
    → Draft personalized reply with next step (demo link, calendar link)
    → Quality gate check (personalization, tone, CTA)
    → Create as "[AUTO-APPROVED]" draft
    → Create Calendar event for demo call
  
  WARM (asked questions):
    → Draft answer using product knowledge + sales.md
    → Include subtle CTA for next step
    → Quality gate check
    → Create as "[AUTO-APPROVED]" draft
  
  COLD ("not now" or "not interested"):
    → Draft polite acknowledgment
    → Add to 30-day follow-up sequence
    → Calendar reminder for re-engagement
    → Create as "[AUTO-APPROVED]" draft

  NEGATIVE (complaint, angry):
    → Flag as "[NEEDS HUMAN REVIEW]" — NEVER auto-respond to complaints
    → Present the situation and suggested response for your decision

STEP 3: SUMMARY (AI — automated)
  → "Today: 3 responses received. 1 HOT (demo request from {Name}),
     1 WARM (pricing question from {Name}), 1 COLD ({Name} said later).
     All replies drafted and ready. Demo call scheduled for Thursday 2pm."

YOUR ROLE: Open Gmail, scan the subjects, hit send. 2 minutes.
```

### Workflow 4: Ad Auto-Optimization

```
TRIGGER: Weekly OR when performance drops below threshold

STEP 1: PULL DATA (AI via Adspirer — automated)
  → Get campaign performance: impressions, clicks, CTR, conversions, spend

STEP 2: ANALYZE (AI — automated)
  → Compare each ad set against targets
  → Identify: winners (CTR >1.5%, ROAS >2x), losers (CTR <0.5%, no conversions)
  → Calculate: CPA, ROAS, budget efficiency

STEP 3: DECIDE (AI — automated within rules)
  
  AUTO-EXECUTE RULES (no human needed):
    → If ad set CTR < 0.3% for 3+ days → PAUSE
    → If ad set CPA > 2x target for 3+ days → REDUCE BUDGET 50%
    → If winning ad set at budget cap → INCREASE BUDGET 20%
    → If all ad sets underperforming → PAUSE CAMPAIGN + alert human
  
  REQUIRES HUMAN:
    → Launching entirely new campaign (new audience, new budget)
    → Increasing total daily budget above pre-set ceiling
    → Changing targeting or offer strategy

STEP 4: REPORT (AI — automated)
  → "Ad performance this week: Spent $X, generated Y leads at $Z CPA.
     Actions taken: Paused 2 underperforming ad sets, increased budget
     on winner by 20%. ROAS improved from 1.8x to 2.4x."
```

---

## Safety Rails (What NEVER Auto-Executes)

Even with auto-review, some actions always require human judgment:

```
ALWAYS HOLD FOR HUMAN:
  ❌ Responding to complaints, refund requests, or angry messages
  ❌ Any email to more than 50 recipients (bulk send)
  ❌ Spending above pre-set daily/monthly budget limits
  ❌ Content about sensitive topics (legal, health, financial advice)
  ❌ Messages to specific individuals the user flagged as VIP
  ❌ Partnership agreements, contracts, or pricing negotiations
  ❌ Anything that could damage brand reputation if wrong
  ❌ First-time outreach to a new market/segment (unproven messaging)

SAFE TO AUTO-EXECUTE:
  ✅ Personalized cold outreach (1-to-1, quality-gated)
  ✅ Follow-up emails in existing sequences
  ✅ Social media posts (quality-gated)
  ✅ Calendar event creation
  ✅ Ad optimization within pre-set rules
  ✅ Performance reports and dashboards
  ✅ Content drafts saved to files
  ✅ Replies to warm/hot leads (quality-gated)
```

---

## The Auto-Review Architecture

### How Self-Review Actually Works

```
1. GENERATE draft using reference files (content.md, sales.md, etc.)
2. SCORE against quality gate checklist (specific to content type)
3. VERIFY against brand-voice.md (tone, vocabulary, personality)
4. VALIDATE against persona.md (is this relevant to ICP?)
5. CHECK against previous outreach (no duplicates, no spam)
6. ASSIGN status:
   [AUTO-APPROVED]  → Execute immediately
   [REVIEW MINOR]   → Execute but flag the issue
   [NEEDS REVIEW]   → Hold for human, show failures
7. EXECUTE the approved actions via MCP tools
8. LOG everything for weekly review
```

### Quality Scoring Formula

```
Score = (Personalization × 2) + (Brand Voice × 2) + (Value × 2) + 
        (CTA × 1) + (Format × 1) + (Spam Check × 2)

Max score: 20
Auto-send threshold: 16+ (80%)
Review threshold: 12-15 (60-75%)
Reject threshold: <12 (below 60%)
```

---

## The Daily Auto-Pilot Routine

What happens when you say "/marketing-ops daily":

```
MORNING (AI runs autonomously — ~5 min):
  1. ✅ Scan Gmail for responses → auto-triage → draft replies
  2. ✅ Generate 5 new outreach emails → quality gate → create drafts
  3. ✅ Generate today's social post → quality gate → save to publish
  4. ✅ Check ad performance → auto-optimize within rules
  5. ✅ Create calendar events for follow-ups
  6. ✅ Update revenue tracking dashboard

  DELIVERS TO YOU:
  "Good morning. Here's your marketing status:
   - 5 outreach emails auto-sent ✅ (passed quality gate, sent via auto-sender)
   - 2 follow-ups auto-sent ✅
   - 1 hot lead replied — demo reply auto-sent with calendar link ✅
   - 1 draft held for your review ⚠️ (failed personalization check)
   - Today's LinkedIn post ready [copy-paste in 30 sec]
   - Ads: paused 1 underperformer, winner CTR up 12%
   
   Your action: Review 1 held draft. Post LinkedIn content. 
   Take demo call at 2pm. That's it."

YOUR TOTAL TIME: 3 minutes + demo call
AI TOTAL WORK: Prospecting, writing, reviewing, sending, scheduling, optimizing
```

---

## What Still Requires You (And Why)

**Demo calls and customer conversations:**
AI preps you with scripts, prospect research, and objection handling.
But at $0 MRR, the founder's voice builds trust that no AI can replicate.
As you scale past $10K MRR, consider AI chatbots for initial qualification.

**Strategic decisions:**
AI provides data and recommendations. You decide:
- Which product to focus on
- Which market to enter
- Whether to pivot or persevere
- Pricing changes
- Partnership commitments

**The quality of the auto-review depends on the quality of your foundation files.**
If marketing-profile.yml and brand-voice.md are vague, the quality gate
produces vague results. Invest 30 minutes in detailed foundation files
and the auto-pilot becomes dramatically better.

---

## The Revenue Math

```
WITHOUT auto-execution:
  You write 2-3 emails/day manually → 15/week → maybe 2 replies → 0-1 demo
  Time spent: 10+ hours/week on marketing

WITH auto-execution:
  AI writes + reviews 5 emails/day → 25/week → 5-8 replies → 2-3 demos
  AI creates social posts, follow-ups, ad optimization automatically
  Time spent: 30 min/day (3.5 hours/week) — mostly just hitting "send"

  Net result: 2-3× more outreach, 3× more demos, same time investment
  
  At 20% close rate: 2-3 demos/week → ~2 new customers/month
  At $79/mo ARPU: $158/month new MRR from autopilot alone
  In 6 months: $948 MRR growing → compound from there
```

The skill doesn't guarantee results. But it guarantees your outreach
actually reaches human beings instead of sitting in a file nobody reads.
