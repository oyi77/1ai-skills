# Lead Prospecting & Contact Sourcing Reference

You can't send outreach to nobody. This reference covers how to find,
qualify, and build target lists automatically — so the execution engine
always has fresh prospects to contact.

---

## The Prospecting Pipeline

```
DISCOVER            →  QUALIFY           →  ENRICH           →  OUTREACH
Find potential leads    Score against ICP    Find email/contact   Auto-send
(web, social, dirs)     (keep/skip)         (tools + research)   (quality-gated)
```

---

## Source 1: Web Search Prospecting (Free, Immediate)

### How AI Finds Leads Via Web Search

The skill can search the web to find potential leads matching your ICP.
This runs as part of the daily routine automatically.

**Search patterns that find leads:**

```
For B2B SaaS targeting marketing managers:
  "marketing manager" + "{industry}" + "{city}" site:linkedin.com
  "head of marketing" "{company size}" "{industry}"
  "{job title}" "looking for" "{solution category}"

For Indonesian UMKM targeting:
  "pemilik usaha" "{kategori bisnis}" "{kota}" site:instagram.com
  "UMKM" "{produk}" site:tokopedia.com
  "{bisnis}" "kontak" "whatsapp" "{kota}"

For SaaS targeting developers:
  "{technology}" "built with" site:github.com
  "using {competitor}" "alternative" site:reddit.com
  "{role}" "{company}" site:linkedin.com/in/
```

### Extracting Prospect Information
From web search results, extract:
```
- Name (from LinkedIn, company about page, social profile)
- Company (from website, LinkedIn)
- Role/Title (from LinkedIn, bio)
- Email (from website contact page, about page, or derive from pattern)
- Personalization hook (recent post, product launch, hiring signal)
```

---

## Source 2: Social Media Prospecting (Free)

### Reddit Lead Mining
```
Search your product's problem space on Reddit:
  "frustrated with {problem}" — people actively seeking solutions
  "looking for {solution type}" — explicit demand
  "anyone recommend {category}" — buying intent
  "{competitor} alternative" — switching intent
  
Extract: Username → check profile → find their company/website
```

### Twitter/X Lead Mining
```
Search queries:
  "need a {tool/solution} for {problem}"
  "anyone know a good {category}?"
  "switching from {competitor}"
  "built a {type of product}" (find fellow builders for partnerships)
  
Extract: Handle → bio → website → contact
```

### LinkedIn Lead Mining (Via Web Search)
```
Search: site:linkedin.com/in/ "{job title}" "{company}" "{location}"

The web search returns LinkedIn profiles. Extract:
- Name and title
- Company and size
- Recent posts/activity (for personalization)
- Email pattern from company domain (firstname@company.com)
```

### Instagram Lead Mining (For Consumer/UMKM)
```
Search: site:instagram.com "{business category}" "{city}"
  
For Indonesian UMKM:
  "{kategori}" "{kota}" site:instagram.com
  Look for: business accounts with contact buttons, email in bio,
  WhatsApp links in bio
```

---

## Source 3: Directory & Database Prospecting

### Free Sources
| Source | Best For | How to Access |
|--------|----------|--------------|
| Google Maps | Local businesses | Search "{business type} near {city}" |
| LinkedIn (web search) | B2B prospects | site:linkedin.com searches |
| GitHub | Developer/technical leads | Search repos, contributors, stars |
| Product Hunt | SaaS founders/early adopters | Browse launches in your category |
| IndieHackers | Solo founders | Browse profiles, projects |
| Shopee/Tokopedia seller pages | Indonesian sellers | Browse seller listings |
| Facebook Groups | Community members | Join relevant groups |

### Paid Sources (When You Have Budget)
| Tool | Cost | Volume | Quality |
|------|------|--------|---------|
| Apollo.io | Free tier + $49/mo | 200 emails/mo free | High (verified emails) |
| Hunter.io | Free tier + $49/mo | 50 searches/mo free | High (email patterns) |
| Snov.io | Free tier + $30/mo | 50 credits/mo free | Medium-High |
| Clearbit | Custom | Unlimited | Very High |
| PhantomBuster | $69/mo | LinkedIn/social scraping | High |

---

## Source 4: Existing Contact Mining (Warmest Leads)

### Gmail Contact Mining
Before cold outreach, mine your existing network:

```
Use Gmail:search_threads to find:
  1. People who emailed you about the problem you solve
     → Search: "{problem keywords}" in:inbox
  
  2. People who asked about your product/service
     → Search: "{product name}" OR "{service}" in:inbox
  
  3. Old conversations that went cold
     → Search: "interested" OR "let's talk" older_than:30d
  
  4. People in relevant industries
     → Search: from:{industry domain patterns}

These are WARM leads — much higher conversion than cold outreach.
Prioritize re-engagement over cold prospecting.
```

### Social Following Mining
- Check your Twitter/X followers who match ICP
- Check LinkedIn connections in target roles
- Check Instagram business followers
- Check WhatsApp contacts in business groups

---

## Email Finding Methods

### Method 1: Email Pattern Guessing
Most companies use predictable email patterns:
```
firstname@company.com         (most common — ~60% of companies)
firstname.lastname@company.com  (second most common — ~25%)
f.lastname@company.com
firstnamelastname@company.com
first@company.com

Steps:
1. Find their name and company domain
2. Try the most common patterns
3. Verify with a free tool (Hunter.io email verifier)
```

### Method 2: Website Contact Page
```
Check their website:
  /contact
  /about
  /team
  Footer (often has email)
  
For UMKM: Check Instagram bio for WhatsApp number or email
```

### Method 3: Free Email Finding Tools
```
Hunter.io         — 25 free searches/month, find email by domain
Snov.io           — 50 free credits/month
Clearbit Connect  — Chrome extension, free tier
RocketReach       — Limited free searches
```

### Method 4: Social Profile Email
```
Many people list email in:
  - Twitter/X bio
  - LinkedIn "Contact info" section
  - GitHub profile
  - Instagram bio (especially business accounts)
  - Personal website
```

---

## Lead Qualification (Auto-Score)

Every discovered prospect gets auto-scored before outreach:

```
SCORE EACH (1-5):

ICP MATCH: Does their role/company/industry match your persona.md?
  5 = Exact match (right role, right company size, right industry)
  3 = Partial match (right industry but wrong role, or vice versa)
  1 = Poor match (different market entirely)

SIGNAL STRENGTH: How strong is the buying intent signal?
  5 = Actively looking for solution ("need a tool for X")
  4 = Expressing frustration with current approach
  3 = In the right industry/role (inferred need)
  2 = Tangentially related
  1 = No signal, just matching demographics

REACHABILITY: Can we actually contact them?
  5 = Email found and verified
  4 = Email found but unverified
  3 = WhatsApp/DM available
  2 = LinkedIn only (lower response rate)
  1 = No direct contact method

PERSONALIZATION POTENTIAL: Can we write a genuinely personal email?
  5 = Found recent post/content/activity to reference
  3 = Know their company and role, can mention specifics
  1 = Just a name and email — generic only

TOTAL: /20
  16-20 → HIGH PRIORITY: Include in today's outreach
  10-15 → MEDIUM: Include if daily quota not filled
  <10   → LOW: Skip or save for later
```

---

## Automated Daily Prospecting Workflow

This is what happens inside the execution engine's Step 1:

```
INPUT: ICP from persona.md + lead_sources from marketing-profile.yml

1. SEARCH (AI via web search)
   → Run 3-5 search queries based on ICP
   → Collect 10-15 potential prospects
   → Extract: name, company, role, website

2. DEDUPLICATE
   → Check Gmail: have we contacted this person before?
   → Check tracking log: is this person in our pipeline?
   → Remove duplicates

3. QUALIFY (Auto-score)
   → Score each prospect (ICP match, signal, reachability, personalization)
   → Rank by score
   → Take top 5 for today

4. ENRICH
   → Find email address (pattern guess + verify)
   → Find personalization hook (recent post, company news, product update)
   → Prepare outreach context

5. OUTPUT → Feed into outreach pipeline
   → 5 qualified prospects with:
     - Name, email, company, role
     - Personalization hook
     - Recommended email angle
   → Ready for the drafting → quality gate → send pipeline
```

---

## Prospect Tracking

### Keep a Running List

Every prospect goes into a tracking document:

```markdown
## Prospect Pipeline — {Date}

| Name | Company | Email | Source | Score | Status | Last Contact | Next Action |
|------|---------|-------|--------|-------|--------|-------------|-------------|
| {name} | {co} | {email} | Reddit | 18/20 | Sent Email 1 | Apr 10 | Follow up Apr 13 |
| {name} | {co} | {email} | LinkedIn | 15/20 | Responded - Interested | Apr 9 | Demo Apr 12 |
| {name} | {co} | {email} | Web | 12/20 | No response | Apr 7 | Breakup email Apr 14 |
```

### Status Flow
```
PROSPECTED → CONTACTED → RESPONDED → DEMO → PROPOSAL → WON/LOST
                  ↓                                        ↓
            No Response                               LOST REASON:
            → Follow-up #2                            (price/timing/
            → Follow-up #3                             fit/competitor)
            → Breakup                                  ↓
            → 30-day re-engage                      Win-back sequence
```

---

## Indonesian Market Prospecting (UMKM)

### Where to Find Indonesian Business Leads

```
1. Google Maps: "{jenis usaha}" + "{kota}"
   → Businesses with phone numbers, websites, reviews
   
2. Shopee/Tokopedia Seller Pages:
   → Browse "{kategori}" sellers → check their profile for WhatsApp/email
   
3. Instagram: Search #{kota}{bisnis} (e.g., #surabayakuliner)
   → Business accounts with contact buttons
   
4. WhatsApp Groups: Join industry-specific groups
   → Members are potential leads (but DON'T spam — provide value first)
   
5. Facebook Groups: "{industri}" + "{kota}" groups
   → Active members who post about business challenges

6. Google: "{jenis bisnis}" "whatsapp" "{kota}"
   → Businesses that list WhatsApp = ready for direct contact
```

### WhatsApp Outreach for Indonesian Market
```
WhatsApp is the primary business channel in Indonesia.
Outreach format:

"Assalamualaikum/Halo Pak/Bu {nama},

Saya {nama Anda} dari {bisnis Anda}.
Saya lihat {toko/bisnis mereka} di {platform} — {pujian spesifik}.

Kami punya {solusi} yang bisa bantu {masalah spesifik mereka}.
{Bukti: pelanggan lain sudah pakai dan hasilnya...}

Boleh saya jelaskan lebih lanjut? Cuma 5 menit. 🙏

Terima kasih,
{nama Anda}"

Rules:
  - Always greet appropriately (Pak/Bu, Kak)
  - Be specific about WHY you're contacting THEM
  - Keep it short (WhatsApp = mobile = short attention span)
  - Include social proof if possible
  - End with low-friction CTA ("Cuma 5 menit")
```
