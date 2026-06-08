"""
Module 2: ContentPlanner — 7-day content calendar and optimal timing.
Single Responsibility: scheduling logic only. No caption gen, no quality.
Open/Closed: add pillars/events in constants below — no class changes.

Imports Scheduler from: content/content-generator/scripts/scheduler.py
Pillars from: notes/paperclip-content-strategy.md (5-pillar system)
Times: Indonesian audience research (WIB = UTC+7)
"""

import sys

sys.path.insert(0, "/home/openclaw/.openclaw/workspace")

import random
from datetime import date, timedelta
from dataclasses import dataclass, field

try:
    from content.content_generator.scripts.scheduler import Scheduler, Schedule

    _SCHEDULER_AVAILABLE = True
except ImportError:
    _SCHEDULER_AVAILABLE = False
    Scheduler = None  # type: ignore

try:
    from .base import BaseModule
except ImportError:
    from base import BaseModule  # standalone


# ── Constants (Open/Closed: extend here, no class changes needed) ─────────

CONTENT_PILLARS = [
    "AI for Business Growth",
    "Digital Marketing Mastery",
    "Future of Work & AI Talent",
    "Tech for Non-Technical Founders",
    "BerkahKarya Insider",
]

# Indonesian audience optimal times (WIB 24h, sourced from platform analytics)
OPTIMAL_TIMES: dict[str, list[str]] = {
    "tiktok": ["11:00", "12:00", "19:00", "20:00", "21:00"],
    "instagram": ["08:00", "09:00", "12:00", "13:00", "18:00", "19:00", "20:00"],
    "facebook": ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00"],
    "youtube": ["14:00", "15:00", "16:00", "17:00", "20:00", "21:00", "22:00"],
    "x": ["08:30", "12:00", "14:00", "17:00", "20:30"],
}

INDONESIAN_EVENTS: list[dict] = [
    {"name": "Ramadan", "month": 3, "day": 1, "type": "religious"},
    {"name": "Lebaran / Eid", "month": 4, "day": 1, "type": "religious"},
    {"name": "Hari Pancasila", "month": 6, "day": 1, "type": "national"},
    {"name": "Harbolnas 6.6", "month": 6, "day": 6, "type": "ecommerce"},
    {"name": "Harbolnas 7.7", "month": 7, "day": 7, "type": "ecommerce"},
    {"name": "Harbolnas 8.8", "month": 8, "day": 8, "type": "ecommerce"},
    {"name": "Kemerdekaan RI", "month": 8, "day": 17, "type": "national"},
    {"name": "Harbolnas 9.9", "month": 9, "day": 9, "type": "ecommerce"},
    {"name": "Harbolnas 10.10", "month": 10, "day": 10, "type": "ecommerce"},
    {"name": "Harbolnas 11.11", "month": 11, "day": 11, "type": "ecommerce"},
    {"name": "Harbolnas 12.12", "month": 12, "day": 12, "type": "ecommerce"},
    {"name": "Tahun Baru", "month": 1, "day": 1, "type": "general"},
]


@dataclass
class ContentSlot:
    date: str
    time: str  # HH:MM WIB
    platform: str
    pillar: str
    persona_id: str
    product_id: str | None = None
    notes: str = ""


@dataclass
class WeeklyCalendar:
    week_start: str
    slots: list[ContentSlot] = field(default_factory=list)

    def by_day(self) -> dict[str, list[ContentSlot]]:
        out: dict[str, list[ContentSlot]] = {}
        for s in self.slots:
            out.setdefault(s.date, []).append(s)
        return out

    def summary(self) -> str:
        by_day = self.by_day()
        lines = [f"Weekly Calendar — {self.week_start} ({len(self.slots)} slots)"]
        for day in sorted(by_day):
            lines.append(f"\n  {day}:")
            for s in by_day[day]:
                lines.append(f"    {s.time} | {s.platform:<12} | {s.pillar[:35]}")
        return "\n".join(lines)


class ContentPlanner(BaseModule):
    """Generate weekly/daily content calendars with pillar rotation."""

    def __init__(self, config: dict):
        super().__init__(config)
        self._pillar_idx = 0
        self.scheduler = Scheduler(check_interval=60) if _SCHEDULER_AVAILABLE else None

    # ── Public API ────────────────────────────────────────────────────────

    def generate_weekly_calendar(
        self,
        products: list[dict],
        personas: list[dict],
        platforms: list[str],
    ) -> WeeklyCalendar:
        """Build a 7-day content plan starting from today."""
        today = date.today()
        cal = WeeklyCalendar(week_start=today.isoformat())
        for offset in range(7):
            day = today + timedelta(days=offset)
            cal.slots.extend(
                self.generate_daily_plan(day, products, personas, platforms)
            )
        return cal

    def generate_daily_plan(
        self,
        day: date,
        products: list[dict] | None = None,
        personas: list[dict] | None = None,
        platforms: list[str] | None = None,
    ) -> list[ContentSlot]:
        """Generate 2 posting slots per platform for the given day."""
        products = products or self.config.get("products", [])
        personas = personas or self.config.get("personas", [])
        platforms = platforms or [
            k for k, v in self.config.get("platforms", {}).items() if v.get("enabled")
        ]

        slots: list[ContentSlot] = []
        for platform in platforms:
            times = self.get_optimal_times(platform)
            for t in times[:2]:
                persona = self._pick_persona(personas, platform)
                product = self._pick_product(products)
                slots.append(
                    ContentSlot(
                        date=day.isoformat(),
                        time=t,
                        platform=platform,
                        pillar=self.rotate_pillars([]),
                        persona_id=persona["id"] if persona else "jendralbot_main",
                        product_id=product["id"] if product else None,
                    )
                )
        return slots

    def get_optimal_times(self, platform: str) -> list[str]:
        """Return optimal WIB posting times. Config overrides constants."""
        return self.config.get("schedule", {}).get(platform) or OPTIMAL_TIMES.get(
            platform, ["09:00", "19:00"]
        )

    def rotate_pillars(self, history: list[str]) -> str:
        """Return next pillar, avoiding immediate repeats."""
        recent = set(history[-(len(CONTENT_PILLARS) - 1) :])
        candidates = [p for p in CONTENT_PILLARS if p not in recent] or CONTENT_PILLARS
        pillar = candidates[self._pillar_idx % len(candidates)]
        self._pillar_idx += 1
        return pillar

    def seasonal_events(self, lookahead_days: int = 30) -> list[dict]:
        """Return upcoming Indonesian events within lookahead_days."""
        today = date.today()
        cutoff = today + timedelta(days=lookahead_days)
        return [
            {**e, "date": date(today.year, e["month"], e["day"]).isoformat()}
            for e in INDONESIAN_EVENTS
            if today <= date(today.year, e["month"], e["day"]) <= cutoff
        ]

    # ── Private ───────────────────────────────────────────────────────────

    def _pick_persona(self, personas: list[dict], platform: str) -> dict | None:
        compat = [p for p in personas if platform in p.get("platforms", [])]
        pool = compat or personas
        return random.choice(pool) if pool else None

    def _pick_product(self, products: list[dict]) -> dict | None:
        weights_cfg = self.config.get("product_weights", {})
        if weights_cfg and products:
            pool = [p for p in products if p["id"] in weights_cfg]
            if pool:
                return random.choices(
                    pool, weights=[weights_cfg[p["id"]] for p in pool], k=1
                )[0]
        return random.choice(products) if products else None


# ── Self-test ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from base import load_config  # noqa (standalone)

    cfg = load_config()
    planner = ContentPlanner(cfg)

    print("=== Optimal Times ===")
    for plat in ["tiktok", "instagram", "facebook", "youtube"]:
        print(f"  {plat}: {planner.get_optimal_times(plat)}")

    print("\n=== Pillar Rotation (8 calls) ===")
    history: list[str] = []
    for _ in range(8):
        p = planner.rotate_pillars(history)
        history.append(p)
        print(f"  → {p}")
    assert len(set(history)) == len(CONTENT_PILLARS), "All pillars should appear"

    print("\n=== Seasonal Events (next 90 days) ===")
    events = planner.seasonal_events(90)
    if events:
        for e in events:
            print(f"  {e['date']} — {e['name']}")
    else:
        print("  (none in next 90 days)")

    print("\n=== Weekly Calendar (tiktok + instagram) ===")
    cal = planner.generate_weekly_calendar(
        products=cfg["products"],
        personas=cfg["personas"],
        platforms=["tiktok", "instagram"],
    )
    print(cal.summary())

    print(f"\n  Scheduler available: {_SCHEDULER_AVAILABLE}")
    print("✅ content_planner self-test passed")
