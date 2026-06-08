"""
Module 6: EngagementEngine (Buzzer)
NEW module: no equivalent in existing codebase.

Goal: coordinate multi-account engagement with natural timing to trigger algo amplification.
Timing strategy: seed (2-5min) → early wave (15-30min) → mid (1-2h) → sustain (3-6h).
"""

import json
import random
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

try:
    from .base import BaseModule, load_config
except ImportError:
    import os as _os

    _CFG_PATH = _os.path.join(_os.path.dirname(__file__), "../config.json")

    def load_config(path=_CFG_PATH):
        with open(_os.path.abspath(path)) as f:
            return json.load(f)

    class BaseModule:
        def __init__(self, config):
            self.config = config

        def platform_cfg(self, p):
            return self.config.get("platforms", {}).get(p, {})


# ── TIMING WAVES ──────────────────────────────────────────────────────────────
WAVES = [
    {"name": "seed", "min_min": 2, "max_min": 5, "actions": ["like"], "ratio": 1.0},
    {
        "name": "early",
        "min_min": 15,
        "max_min": 30,
        "actions": ["like", "comment"],
        "ratio": 0.6,
    },
    {
        "name": "mid",
        "min_min": 60,
        "max_min": 120,
        "actions": ["like", "comment", "share"],
        "ratio": 0.4,
    },
    {
        "name": "sustain",
        "min_min": 180,
        "max_min": 360,
        "actions": ["like", "comment"],
        "ratio": 0.3,
    },
]

# Authentic-looking comment bank by post type
COMMENT_BANK = {
    "promo": [
        "Wah info menarik nih! 👆",
        "Harga segitu worth it!",
        "Langsung cek!",
        "Menarik banget!",
    ],
    "tutorial": [
        "Tutorial keren banget!",
        "Auto saved! 🔖",
        "Dicoba ah!",
        "Bermanfaat banget 💡",
    ],
    "motivation": [
        "Semangat terus! 💪",
        "Setuju banget ini!",
        "Relate banget 😭",
        "Facts!",
    ],
    "product": [
        "Wah ini berguna!",
        "Perlu nih!",
        "Mantap jiwa 🔥",
        "Makasih infonya 🙏",
    ],
    "default": ["Keren! 🔥", "Mantap!", "Good info!", "👍", "Setuju!"],
}

# Account warm-up: gradual activity increase over days
WARMUP_PHASES = [
    {"day_from": 1, "day_to": 2, "daily": 5, "types": ["like"]},
    {"day_from": 3, "day_to": 5, "daily": 12, "types": ["like", "comment"]},
    {"day_from": 6, "day_to": 10, "daily": 25, "types": ["like", "comment", "follow"]},
]


class EngagementEngine(BaseModule):
    """
    Build natural-looking engagement schedules for multi-account boosting.
    Produces schedules (dicts) — execution is the caller's responsibility.
    """

    def __init__(self, config: dict):
        super().__init__(config)
        _logs = Path(config.get("paths", {}).get("logs_dir", "/tmp/ck_logs"))
        _logs.mkdir(parents=True, exist_ok=True)
        self._schedule_file = _logs / "engagement_schedule.json"
        self._log_file = _logs / "engagement_engine.jsonl"

    # ── PUBLIC ────────────────────────────────────────────────────────────────

    def boost_new_post(self, post_id: str, accounts: List[str]) -> Dict:
        """
        Build engagement schedule across all waves for a new post.
        Returns schedule dict; saves to disk. Does NOT execute.
        """
        schedule, now = [], datetime.now()
        for wave in WAVES:
            n = max(1, int(len(accounts) * wave["ratio"]))
            wave_accounts = random.sample(accounts, min(n, len(accounts)))
            for i, acct in enumerate(wave_accounts):
                base = random.randint(wave["min_min"], wave["max_min"])
                jitter = random.randint(0, 4) + i * 2
                schedule.append(
                    {
                        "post_id": post_id,
                        "account_id": acct,
                        "action": random.choice(wave["actions"]),
                        "wave": wave["name"],
                        "trigger_at": (
                            now + timedelta(minutes=base + jitter)
                        ).isoformat(),
                        "executed": False,
                    }
                )
        self._append_schedule(schedule)
        print(
            f"[EngagementEngine] {len(schedule)} actions scheduled for {post_id} across {len(WAVES)} waves"
        )
        return {
            "post_id": post_id,
            "total_actions": len(schedule),
            "schedule": schedule,
        }

    def schedule_engagement(self, post_id: str, delay_minutes: int) -> Dict:
        """Schedule a single like action at post_id after delay_minutes."""
        trigger = datetime.now() + timedelta(minutes=delay_minutes)
        action = {
            "post_id": post_id,
            "action": "like",
            "wave": "manual",
            "trigger_at": trigger.isoformat(),
            "executed": False,
        }
        self._append_schedule([action])
        return action

    def generate_natural_comment(
        self, post_content: str, persona: str = "default"
    ) -> str:
        """Pick authentic-looking comment based on detected post type."""
        t = post_content.lower()
        if any(w in t for w in ["beli", "harga", "promo", "diskon", "gratis"]):
            pool = COMMENT_BANK["promo"]
        elif any(w in t for w in ["cara", "tutorial", "tips", "langkah"]):
            pool = COMMENT_BANK["tutorial"]
        elif any(w in t for w in ["semangat", "sukses", "motivasi", "mindset"]):
            pool = COMMENT_BANK["motivation"]
        elif any(w in t for w in ["produk", "tools", "aplikasi"]):
            pool = COMMENT_BANK["product"]
        else:
            pool = COMMENT_BANK["default"]

        comment = random.choice(pool)
        if "jendral" in persona.lower() and random.random() > 0.5:
            comment += " ⚔️"
        return comment

    def warm_up_account(self, account_id: str) -> Dict:
        """
        Build a gradual warm-up action plan for a new account (10-day ramp).
        Returns plan dict — caller schedules actual execution.
        """
        plan, now = [], datetime.now()
        for phase in WARMUP_PHASES:
            for day in range(phase["day_from"], phase["day_to"] + 1):
                for n in range(phase["daily"]):
                    # Space actions through waking hours (08:00–22:00)
                    hour = 8 + (n * 50 // 60) % 14
                    minute = (n * 50) % 60
                    run_at = (now + timedelta(days=day)).replace(
                        hour=hour, minute=minute, second=0
                    )
                    plan.append(
                        {
                            "account_id": account_id,
                            "action": random.choice(phase["types"]),
                            "at": run_at.isoformat(),
                            "phase": f"day{phase['day_from']}",
                        }
                    )
        print(
            f"[EngagementEngine] Warm-up plan: {len(plan)} actions over 10 days for {account_id}"
        )
        return {"account_id": account_id, "total": len(plan), "plan": plan}

    def get_engagement_schedule(self) -> List[Dict]:
        """Return all pending (not executed) scheduled actions."""
        if not self._schedule_file.exists():
            return []
        with open(self._schedule_file) as f:
            return [a for a in json.load(f) if not a.get("executed")]

    def cross_promote(self, post_id: str, platforms: List[str]) -> Dict:
        """Build cross-promotion info per platform. Caller handles PostBridge calls."""
        result = {}
        for p in platforms:
            accounts = self.platform_cfg(p).get("account_ids", [])
            result[p] = {
                "post_id": post_id,
                "accounts": len(accounts),
                "status": "ready" if accounts else "no_accounts",
            }
        print(f"[EngagementEngine] Cross-promote {post_id}: {list(result.keys())}")
        return result

    # ── PRIVATE ───────────────────────────────────────────────────────────────

    def _append_schedule(self, new_actions: List[Dict]):
        existing = self.get_engagement_schedule()
        with open(self._schedule_file, "w") as f:
            json.dump(existing + new_actions, f, ensure_ascii=False, indent=2)


# ── STANDALONE TEST ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = load_config()
    ee = EngagementEngine(cfg)
    accounts = [f"acc_{i:03d}" for i in range(1, 7)]

    print("=" * 55 + "\nENGAGEMENT ENGINE — Test\n" + "=" * 55)

    result = ee.boost_new_post("post_test123", accounts)
    print(f"\n🚀 Boosted: {result['total_actions']} actions scheduled")
    for a in result["schedule"][:4]:
        print(
            f"  [{a['wave']:8}] {a['account_id']} → {a['action']} @ {a['trigger_at'][11:16]}"
        )
    print(f"  ... +{result['total_actions']-4} more")

    comment = ee.generate_natural_comment(
        "Tutorial cara bikin konten viral pakai AI", "jendralbot_main"
    )
    print(f"\n💬 Natural comment: '{comment}'")

    warm = ee.warm_up_account("new_account_007")
    print(f"🌡️  Warm-up: {warm['total']} actions, first: {warm['plan'][0]}")

    pending = ee.get_engagement_schedule()
    print(f"📋 Pending in schedule: {len(pending)}")

    cross = ee.cross_promote("post_test123", ["tiktok", "instagram", "facebook"])
    print(f"🔗 Cross-promote: {cross}")
