#!/usr/bin/env python3
"""
outreach.py — Warm DM outreach automation with lead scoring.

Features:
  - Warm, personalized DM sequences (NOT spam)
  - Follow-up automation with context-aware personalization
  - Lead scoring from engagement signals
  - CTA templates per platform (TikTok, Instagram, X, LinkedIn)
  - State tracking to avoid double-messaging

Usage:
    python3 outreach.py --lead @username --platform instagram --sequence intro
    python3 outreach.py --import leads.json
    python3 outreach.py --followups          # Process all due follow-ups
    python3 outreach.py --score @username   # Calculate lead score
    python3 outreach.py --stats             # Show pipeline overview

Lead file format (leads.json):
    [
        {
            "handle": "@username",
            "platform": "instagram",
            "name": "Sarah",
            "niche": "fitness",
            "engagement_signals": {
                "liked_posts": 3,
                "commented": true,
                "shared": false,
                "followed_you": true
            },
            "notes": "Asked about pricing in comments",
            "sequence": "intro"
        }
    ]
"""

import json
import os
import sys
import time
import random
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import requests

# ─── Configuration ────────────────────────────────────────────────────────────

BYTEPLUS_API_URL = "https://ark.ap-southeast.bytepluses.com/api/v3/chat/completions"
BYTEPLUS_API_KEY = os.environ.get("BYTEPLUS_API_KEY", "cac5cfc1-e30f-47bb-b8b8-e861ffda28ea")
BYTEPLUS_MODEL   = "seed-1-6-250915"

DATA_DIR     = Path(__file__).parent.parent / "data"
LEADS_FILE   = DATA_DIR / "leads.json"
LOG_FILE     = DATA_DIR / "outreach.log"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("outreach")


# ─── Lead Scoring ─────────────────────────────────────────────────────────────

class LeadScorer:
    """
    Scores leads 0-100 based on engagement signals.

    Score buckets:
      80-100: 🔥 Hot — DM immediately
      60-79:  🌡️  Warm — Queue for intro DM
      40-59:  ⚪ Cool — Nurture with content first
      0-39:   ❄️  Cold — Not ready yet
    """

    SIGNAL_WEIGHTS = {
        "followed_you":           25,  # They followed you — strong signal
        "commented":              20,  # Commented on your posts
        "saved_post":             15,  # Saved (Instagram)
        "liked_posts_3plus":      15,  # Liked 3+ of your posts
        "liked_posts_1":           5,  # Liked at least 1
        "shared":                 15,  # Shared your content
        "replied_to_story":       10,  # Replied to a story
        "asked_question":         20,  # Asked a question in comments
        "mentioned_price":        25,  # Mentioned pricing/cost
        "mentioned_problem":      15,  # Mentioned a relevant problem
        "dm_opened_before":       -10, # Already DMed — reduce (don't double)
        "already_customer":      -100, # Skip existing customers
    }

    @classmethod
    def score(cls, engagement_signals: dict, notes: str = "") -> dict:
        """Calculate lead score from engagement signals."""
        raw_score = 0

        for signal, weight in cls.SIGNAL_WEIGHTS.items():
            if engagement_signals.get(signal, False):
                raw_score += weight

        # Boost from notes keywords
        note_lower = notes.lower()
        if any(w in note_lower for w in ["price", "cost", "how much", "harga"]):
            raw_score += 20
        if any(w in note_lower for w in ["interested", "tell me more", "where can i"]):
            raw_score += 15
        if any(w in note_lower for w in ["problem", "struggle", "help", "need"]):
            raw_score += 10

        score = max(0, min(100, raw_score))

        if score >= 80:
            tier, emoji = "hot", "🔥"
        elif score >= 60:
            tier, emoji = "warm", "🌡️"
        elif score >= 40:
            tier, emoji = "cool", "⚪"
        else:
            tier, emoji = "cold", "❄️"

        return {
            "score": score,
            "tier": tier,
            "emoji": emoji,
            "action": cls._recommended_action(tier),
        }

    @staticmethod
    def _recommended_action(tier: str) -> str:
        return {
            "hot":  "DM immediately with intro + soft CTA",
            "warm": "Queue intro DM within 24h",
            "cool": "Engage with their content 3-5x first, then DM",
            "cold": "Add to nurture list, engage organically",
        }[tier]


# ─── DM Sequence Templates ────────────────────────────────────────────────────

# Platform-specific CTA templates
PLATFORM_CTAS = {
    "tiktok": {
        "soft":   "Drop a 🙋 in the comments if you want me to share more!",
        "medium": "Check the link in my bio — I put together a free guide on this.",
        "direct": "Want to hop on a quick 15-min call? My DMs are open 📲",
    },
    "instagram": {
        "soft":   "Saved to share with someone who needs this? Let me know! 👇",
        "medium": "I made a free resource for exactly this — DM me 'GUIDE' and I'll send it over.",
        "direct": "If this resonates, I have a spot open for a free strategy call this week.",
    },
    "twitter": {
        "soft":   "Retweet if you agree — would love to hear your take.",
        "medium": "I wrote a longer breakdown on this — want me to share the thread?",
        "direct": "Happy to do a quick 1:1 audit of your setup. Slide into my DMs.",
    },
    "linkedin": {
        "soft":   "What's your experience with this? Would love to compare notes.",
        "medium": "I put together a case study on this — happy to share if useful.",
        "direct": "I have a few open slots for a complimentary 20-min strategy session this month.",
    },
}

# DM sequence message templates (fill via AI personalization)
DM_SEQUENCES = {
    "intro": [
        # Day 0: Initial DM
        {
            "day_offset": 0,
            "template": """Hey {name}! 👋

Noticed {personalization_hook}. Really resonated with me.

I {value_statement} — and I think it could genuinely help with {their_problem}.

No pitch here, just thought it was worth a share. {soft_cta}

— {sender_name}""",
        },
        # Day 3: Value DM
        {
            "day_offset": 3,
            "template": """Hey {name}, hope you're well!

Saw you {recent_engagement} — thought you might find this useful:

{value_add}

Curious: what's your biggest challenge with {their_problem} right now?""",
        },
        # Day 7: Direct ask
        {
            "day_offset": 7,
            "template": """Hi {name}!

I've been helping {niche} people like yourself {result}.

Would love to share a quick win I discovered that's working really well.

{direct_cta}

No pressure — just thought it could be valuable for you.""",
        },
        # Day 14: Breakup / last touch
        {
            "day_offset": 14,
            "template": """Hey {name},

I know your inbox is probably slammed — totally get it.

This'll be my last message. I genuinely think {value_statement} and the timing might just not be right.

If anything changes, I'm always here. Wishing you the best with {their_problem}! 🙌

{sender_name}""",
        },
    ],
    "warm": [
        # Shorter sequence for warm leads (already engaged)
        {
            "day_offset": 0,
            "template": """Hey {name}! 👋

Thanks for {engagement_action} — means a lot!

Since you're interested in {niche}, I thought I'd share something I've been working on: {value_statement}.

{direct_cta}""",
        },
        {
            "day_offset": 5,
            "template": """Hey {name}!

Just checking in — did you get a chance to {previous_cta_action}?

Happy to answer any questions or jump on a quick call if easier. {direct_cta}""",
        },
    ],
    "hot": [
        # Aggressive (but warm) sequence for hot leads
        {
            "day_offset": 0,
            "template": """Hey {name}! 🔥

You asked about {price_mention} — I wanted to reach out directly.

Short answer: {price_answer}. But it really depends on your situation.

The fastest way to figure out if it's a fit: {direct_cta}

Takes 15 mins max. Happy to make it worth your time.""",
        },
        {
            "day_offset": 2,
            "template": """Hi {name},

Still have a spot open for this week if you want to chat. {direct_cta}

If you've moved on, no worries at all — just let me know and I'll stop following up! 😊""",
        },
    ],
}


# ─── AI Personalizer ──────────────────────────────────────────────────────────

class DMAIPersonalizer:
    """Use BytePlus AI to personalize DM templates."""

    def __init__(self, api_key: str = BYTEPLUS_API_KEY):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def personalize(
        self,
        template: str,
        lead: dict,
        sender_name: str = "your brand",
        platform: str = "instagram",
        sequence_type: str = "intro",
    ) -> Optional[str]:
        """Personalize a DM template for a specific lead."""

        cta_level = "soft" if sequence_type == "intro" else "medium"
        cta = PLATFORM_CTAS.get(platform, PLATFORM_CTAS["instagram"])[cta_level]

        system_prompt = f"""You write warm, personalized DMs for sales outreach on {platform}.
Rules:
- Sound like a real person, not a marketer
- Reference specific details about the lead
- Be concise — mobile DMs should be short
- No buzzwords, no "I hope this message finds you well"
- No emoji spam — max 2 emojis per message
- The CTA should feel natural, not salesy
- Platform: {platform} (adjust tone accordingly)

Lead info: {json.dumps(lead, indent=2)}
Suggested CTA: {cta}"""

        payload = {
            "model": BYTEPLUS_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Personalize this DM template:\n\n{template}\n\nMake it specific and human. Fill in all placeholders.",
                },
            ],
            "temperature": 0.8,
            "max_tokens": 300,
        }

        try:
            resp = requests.post(BYTEPLUS_API_URL, headers=self.headers, json=payload, timeout=30)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            log.error(f"AI personalization failed: {e}")
            return None


# ─── Lead Database ────────────────────────────────────────────────────────────

class LeadDatabase:
    """Simple JSON-backed lead tracking database."""

    def __init__(self, path: Path = LEADS_FILE):
        self.path = path
        self.data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            with open(self.path) as f:
                return json.load(f)
        return {"leads": {}, "messages_sent": []}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2, default=str)

    def upsert_lead(self, lead: dict) -> dict:
        """Add or update a lead."""
        key = f"{lead['platform']}:{lead['handle']}"
        scoring = LeadScorer.score(
            lead.get("engagement_signals", {}),
            lead.get("notes", ""),
        )
        lead["score"] = scoring["score"]
        lead["tier"]  = scoring["tier"]
        lead["recommended_action"] = scoring["action"]
        lead["added_at"] = lead.get("added_at", datetime.now().isoformat())
        lead["sequence_position"] = lead.get("sequence_position", 0)
        lead["last_contacted_at"] = lead.get("last_contacted_at", None)
        lead["status"] = lead.get("status", "active")
        self.data["leads"][key] = lead
        self._save()
        return lead

    def get_lead(self, handle: str, platform: str) -> Optional[dict]:
        key = f"{platform}:{handle}"
        return self.data["leads"].get(key)

    def get_followups_due(self) -> list[dict]:
        """Return leads with pending follow-up messages due."""
        due = []
        for key, lead in self.data["leads"].items():
            if lead.get("status") != "active":
                continue
            seq_type = lead.get("sequence", "intro")
            seq      = DM_SEQUENCES.get(seq_type, DM_SEQUENCES["intro"])
            pos      = lead.get("sequence_position", 0)
            if pos >= len(seq):
                continue
            last_contacted = lead.get("last_contacted_at")
            if last_contacted is None:
                due.append(lead)
                continue
            next_msg  = seq[pos]
            day_delta = next_msg.get("day_offset", 3)
            due_date  = datetime.fromisoformat(last_contacted) + timedelta(days=day_delta)
            if datetime.now() >= due_date:
                due.append(lead)
        return due

    def record_message_sent(self, lead: dict, message: str):
        """Record that a message was sent to this lead."""
        key = f"{lead['platform']}:{lead['handle']}"
        if key in self.data["leads"]:
            self.data["leads"][key]["last_contacted_at"] = datetime.now().isoformat()
            self.data["leads"][key]["sequence_position"] = lead.get("sequence_position", 0) + 1
        self.data["messages_sent"].append({
            "lead": key,
            "message": message,
            "sent_at": datetime.now().isoformat(),
        })
        self._save()

    def pipeline_stats(self) -> dict:
        tiers = {"hot": 0, "warm": 0, "cool": 0, "cold": 0}
        for lead in self.data["leads"].values():
            tier = lead.get("tier", "cold")
            tiers[tier] = tiers.get(tier, 0) + 1
        return {
            "total": len(self.data["leads"]),
            "by_tier": tiers,
            "messages_sent": len(self.data["messages_sent"]),
            "followups_due": len(self.get_followups_due()),
        }

    def import_leads(self, leads: list[dict]) -> int:
        count = 0
        for lead in leads:
            self.upsert_lead(lead)
            count += 1
        log.info(f"📥 Imported {count} leads")
        return count


# ─── Mock DM Client ───────────────────────────────────────────────────────────

class MockDMClient:
    def send_dm(self, handle: str, platform: str, message: str) -> bool:
        log.info(f"[MOCK] 📨 DM → {handle} on {platform}:")
        for line in message[:200].split("\n"):
            log.info(f"  {line}")
        return True


# ─── Outreach Engine ──────────────────────────────────────────────────────────

class OutreachEngine:
    def __init__(self, sender_name: str = "Alex", dry_run: bool = False):
        self.sender_name = sender_name
        self.dry_run     = dry_run
        self.db          = LeadDatabase()
        self.ai          = DMAIPersonalizer()
        self.dm_client   = MockDMClient()
        log.info(f"🚀 OutreachEngine initialized | sender={sender_name} | dry_run={dry_run}")

    def add_lead(self, lead: dict) -> dict:
        result = self.db.upsert_lead(lead)
        log.info(f"✅ Lead added: {lead['handle']} [{result['tier'].upper()} {result['score']}/100]")
        log.info(f"   Action: {result['recommended_action']}")
        return result

    def send_next_message(self, lead: dict) -> bool:
        """Send the next message in the lead's sequence."""
        seq_type = lead.get("sequence", "intro")
        seq      = DM_SEQUENCES.get(seq_type, DM_SEQUENCES["intro"])
        pos      = lead.get("sequence_position", 0)

        if pos >= len(seq):
            log.info(f"  ✅ {lead['handle']} sequence complete")
            return False

        template = seq[pos]["template"]

        # Personalize with AI
        personalized = self.ai.personalize(
            template=template,
            lead=lead,
            sender_name=self.sender_name,
            platform=lead.get("platform", "instagram"),
            sequence_type=seq_type,
        )

        if not personalized:
            log.warning(f"  ⚠️  Could not personalize message for {lead['handle']}, using template")
            personalized = template

        log.info(f"📨 Sending DM #{pos + 1} to {lead['handle']} ({lead.get('platform', '?')})")

        if not self.dry_run:
            success = self.dm_client.send_dm(
                handle=lead["handle"],
                platform=lead.get("platform", "instagram"),
                message=personalized,
            )
            if success:
                self.db.record_message_sent(lead, personalized)
                return True
            return False
        else:
            log.info(f"[DRY RUN] Would send:\n{personalized}\n")
            self.db.record_message_sent(lead, personalized)
            return True

    def process_followups(self):
        """Process all due follow-up messages."""
        due = self.db.get_followups_due()
        log.info(f"📋 {len(due)} follow-ups due")

        for lead in due:
            self.send_next_message(lead)
            # Small delay between DMs to avoid looking like spam
            delay = random.randint(60, 300)
            log.info(f"⏳ Waiting {delay}s before next DM...")
            if not self.dry_run:
                time.sleep(delay)

    def score_lead(self, handle: str, platform: str) -> dict:
        """Score an existing lead."""
        lead = self.db.get_lead(handle, platform)
        if not lead:
            return {"error": f"Lead {handle} not found on {platform}"}
        return {
            "handle": handle,
            "score": lead.get("score"),
            "tier": lead.get("tier"),
            "recommended_action": lead.get("recommended_action"),
        }

    def import_leads(self, path: str) -> int:
        with open(path) as f:
            leads = json.load(f)
        return self.db.import_leads(leads)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Outreach — Warm DM automation for sales")
    sub    = parser.add_subparsers(dest="cmd")

    # Add lead
    p_add = sub.add_parser("add", help="Add a lead and send initial DM")
    p_add.add_argument("handle")
    p_add.add_argument("--platform", default="instagram")
    p_add.add_argument("--name", default="")
    p_add.add_argument("--niche", default="")
    p_add.add_argument("--notes", default="")
    p_add.add_argument("--sequence", default="intro", choices=["intro", "warm", "hot"])
    p_add.add_argument("--likes", type=int, default=0)
    p_add.add_argument("--commented", action="store_true")
    p_add.add_argument("--followed-you", action="store_true")
    p_add.add_argument("--send", action="store_true", help="Send first DM immediately")
    p_add.add_argument("--dry-run", action="store_true")

    # Follow-ups
    p_fu = sub.add_parser("followups", help="Process due follow-ups")
    p_fu.add_argument("--dry-run", action="store_true")

    # Score
    p_sc = sub.add_parser("score", help="Score a lead")
    p_sc.add_argument("handle")
    p_sc.add_argument("--platform", default="instagram")

    # Import
    p_im = sub.add_parser("import", help="Import leads from JSON file")
    p_im.add_argument("file")
    p_im.add_argument("--dry-run", action="store_true")

    # Stats
    sub.add_parser("stats", help="Show pipeline stats")

    args = parser.parse_args()

    if args.cmd == "add":
        engine = OutreachEngine(dry_run=args.dry_run)
        lead = {
            "handle": args.handle,
            "platform": args.platform,
            "name": args.name or args.handle.lstrip("@"),
            "niche": args.niche,
            "notes": args.notes,
            "sequence": args.sequence,
            "engagement_signals": {
                "liked_posts_1":   args.likes >= 1,
                "liked_posts_3plus": args.likes >= 3,
                "commented":       args.commented,
                "followed_you":    args.followed_you,
            },
        }
        result = engine.add_lead(lead)
        if args.send:
            engine.send_next_message(result)

    elif args.cmd == "followups":
        engine = OutreachEngine(dry_run=args.dry_run)
        engine.process_followups()

    elif args.cmd == "score":
        engine = OutreachEngine()
        result = engine.score_lead(args.handle, args.platform)
        print(json.dumps(result, indent=2))

    elif args.cmd == "import":
        engine = OutreachEngine(dry_run=args.dry_run)
        count = engine.import_leads(args.file)
        print(f"✅ Imported {count} leads")

    elif args.cmd == "stats":
        db = LeadDatabase()
        print(json.dumps(db.pipeline_stats(), indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
