#!/usr/bin/env python3
"""
Full Auto Content Pipeline — Research → Plan → Produce → Review → Publish → Analyze

Runs daily. Each phase is idempotent. State tracked in state.json.

Cron: 06:00 daily → research
      07:30 daily → plan + produce
      09:00 daily → publish
      D+1 08:00  → analyze

Usage:
  python3 full_auto_pipeline.py --phase research
  python3 full_auto_pipeline.py --phase plan
  python3 full_auto_pipeline.py --phase produce
  python3 full_auto_pipeline.py --phase publish
  python3 full_auto_pipeline.py --phase analyze
  python3 full_auto_pipeline.py --all           # run all phases
  python3 full_auto_pipeline.py --status        # show today's state
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import requests

# ── Paths ─────────────────────────────────────────────────────────────────────
WORKSPACE   = Path("/home/openclaw/.openclaw/workspace")
CS_DIR      = WORKSPACE / "content_suite"
PERSONA_DB  = CS_DIR / "personas/persona_database.json"
STATE_FILE  = CS_DIR / "state.json"
LOG_FILE    = CS_DIR / "logs/pipeline.log"
OUTPUT_DIR  = CS_DIR / "output"

# ── Config ────────────────────────────────────────────────────────────────────
POSTBRIDGE_API = "https://api.post-bridge.com/v1"
POSTBRIDGE_KEY = os.getenv("POSTBRIDGE_API_KEY", "pb_live_AT9Xm4PKaYBzAvFZYGgexi")
PB_HDR = {"Authorization": f"Bearer {POSTBRIDGE_KEY}", "Content-Type": "application/json"}

TZ_JAKARTA = timezone(timedelta(hours=7))

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# ── Platform media validation ──────────────────────────────────────────────────
YOUTUBE_ACCTS   = {49678, 49660, 49636, 49639, 49638, 49637, 47691, 47690, 47689}
INSTAGRAM_ACCTS = {49682, 49676, 49661, 49644, 49612, 49640, 49630, 48186, 47681, 49634, 49619, 48374}  # NOTE: 48374 was listed but is tiktok
TIKTOK_ACCTS    = {49663, 49659, 49642, 48372, 48338, 48373, 48374, 48336, 48337, 48335, 45648}
THREADS_ACCTS   = {49683, 49680, 49677, 49662, 49658, 49646, 49641, 49635, 49631, 49618,
                   49614, 49613, 49662}

# PostBridge 500 errors on image posts (verified 2026-03-14):
# - Threads: image POST → 500 (PostBridge not implemented)
# - TikTok: image POST → 500 (PostBridge not implemented)
# Workaround: Threads gets text-only, TikTok skipped until video available
POSTBRIDGE_IMAGE_UNSUPPORTED = THREADS_ACCTS | TIKTOK_ACCTS

def filter_accounts(accounts: list, media_type: Optional[str]) -> list:
    """
    Remove incompatible accounts based on media type.
    media_type: 'video' | 'image' | None (text-only)
    PostBridge verified: Threads+image=500, TikTok+image=500 (server bug, not platform)
    """
    accts = set(accounts)
    removed = []
    if media_type != "video":                    # YouTube: video ONLY
        bad = accts & YOUTUBE_ACCTS
        if bad:
            removed.extend(bad)
            accts -= bad
    if media_type == "image":                    # Threads/TikTok: PostBridge 500 on image
        bad = accts & POSTBRIDGE_IMAGE_UNSUPPORTED
        if bad:
            removed.extend(bad)
            accts -= bad
    if media_type is None:                       # Instagram needs media
        bad = accts & INSTAGRAM_ACCTS
        if bad:
            removed.extend(bad)
            accts -= bad
    if removed:
        log.info(f"  ⚠️  Removed incompatible accounts: {removed} (media_type={media_type})")
    return list(accts)


# ── State management ──────────────────────────────────────────────────────────
def load_state() -> dict:
    today = datetime.now(TZ_JAKARTA).strftime("%Y-%m-%d")
    if STATE_FILE.exists():
        s = json.loads(STATE_FILE.read_text())
        if s.get("date") == today:
            return s
    return {"date": today, "phases": {}, "posts_scheduled": 0, "errors": []}

def save_state(s: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(s, indent=2, ensure_ascii=False))

def load_personas() -> list:
    if not PERSONA_DB.exists():
        log.error(f"Persona DB not found: {PERSONA_DB}")
        return []
    db = json.loads(PERSONA_DB.read_text())
    return db.get("personas", [])


# ── Phase 1: RESEARCH ─────────────────────────────────────────────────────────
def phase_research(state: dict) -> dict:
    """Fetch trending angles for today's content."""
    log.info("🔍 PHASE 1: RESEARCH")
    today = state["date"]
    out_dir = OUTPUT_DIR / today
    out_dir.mkdir(parents=True, exist_ok=True)

    # Trend topics per niche (static pool, rotate daily)
    # In production: replace with TikTok Creative Center API / web scraping
    trend_pool = {
        "trading": [
            "5 Kesalahan Fatal Trader Pemula", "Kenapa 90% Trader Rugi di Tahun Pertama",
            "Cara Baca Chart yang Beneran Works", "Risk Management = Kunci Profit Konsisten",
            "Jurnal Trading: Rahasia Trader Profesional", "Stop Loss itu Bukan Kalah",
            "3 Indikator yang Gue Pakai Setiap Hari", "Psikologi Trading yang Sering Dilupain",
        ],
        "health": [
            "3 Kebiasaan Pagi yang Ubah Hidupku", "Sehat Itu Murah Kalau Tahu Caranya",
            "Tips Jaga Imun di Musim Hujan", "Olahraga 10 Menit per Hari, Ini Hasilnya",
            "Makanan yang Bikin Energi Awet Seharian", "Tidur Berkualitas = Produktivitas 2x",
        ],
        "review": [
            "Review Jujur: Produk Digital yang Gue Coba", "Worth It Gak? Aku Buktiin Dulu",
            "3 Tools yang Bantu Aku Hemat 5 Jam per Minggu", "Honest Review: Beneran Works atau Hype?",
            "Sebelum Beli, Tonton Ini Dulu", "Perbandingan: Mana yang Lebih Bagus?",
        ],
        "digital_marketing": [
            "Cara Dapet 1000 Followers Pertama Tanpa Ads", "Content Strategy yang Benar-Benar Bekerja",
            "3 Kesalahan Content Creator yang Bikin Stuck", "Algoritma TikTok 2026: Yang Perlu Kamu Tahu",
            "Dari 0 ke 10K Followers: Step by Step", "Content Calendar: Kenapa Kamu Butuh Ini",
            "AI Tools yang Wajib Dipake Content Creator", "Cara Monetize Konten dari Hari Pertama",
        ],
        "food": [
            "Resep Simpel Tapi Kelihatan Mewah", "Masak 30 Menit untuk Seminggu",
            "Rahasia Masakan Enak: 3 Bumbu Wajib", "Menu Hemat tapi Tetap Bergizi",
        ],
        "fashion": [
            "Outfit Modis dengan Budget Rp200K", "3 Warna yang Cocok untuk Semua Kulit",
            "Capsule Wardrobe untuk Kantoran", "OOTD Simpel tapi Elegan",
        ],
        "ai_creator": [
            "AI Prompt yang Langsung Kerja untuk Konten", "Cara Pakai AI Buat Bikin Konten 10x Lebih Cepat",
            "3 AI Tools Gratis yang Powerful Banget", "Otomasi Konten dengan AI: Panduan Pemula",
            "ChatGPT vs Claude vs Gemini: Mana yang Terbaik?", "Prompt Engineering untuk Content Creator",
        ],
        "entertainment": [
            "Fakta Mengejutkan yang Baru Aku Tahu", "Hal yang Sering Salah Dipahami Orang",
            "Tips Hidup yang Simpel tapi Powerful", "3 Hal yang Bikin Hidupmu Lebih Mudah",
        ],
    }

    # Rotate based on day of week (deterministic per day)
    day_seed = int(today.replace("-", ""))
    result = {}
    for niche, topics in trend_pool.items():
        random.seed(day_seed + hash(niche))
        result[niche] = random.sample(topics, min(3, len(topics)))

    trend_file = out_dir / "trends.json"
    trend_file.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    log.info(f"  ✅ Trends saved: {trend_file}")
    state["phases"]["research"] = {"status": "done", "file": str(trend_file)}
    return state


# ── Phase 2: PLAN ─────────────────────────────────────────────────────────────
def phase_plan(state: dict) -> dict:
    """Create content plan per persona for today."""
    log.info("📋 PHASE 2: PLAN")
    today = state["date"]
    out_dir = OUTPUT_DIR / today
    trend_file = out_dir / "trends.json"

    if not trend_file.exists():
        log.warning("  Trends not found, running research first")
        state = phase_research(state)

    trends = json.loads(trend_file.read_text())
    personas = load_personas()
    if not personas:
        log.error("  ❌ No personas loaded")
        state["phases"]["plan"] = {"status": "error", "error": "no personas"}
        return state

    plan = []
    for persona in personas:
        if persona.get("skip", False):
            continue
        niche = persona.get("niche", "entertainment")
        niche_trends = trends.get(niche, trends.get("entertainment", []))
        if not niche_trends:
            continue
        random.seed(int(today.replace("-", "")) + hash(persona["persona_id"]))
        headline = random.choice(niche_trends)
        posts_per_day = persona.get("content", {}).get("posts_per_day", 2)
        posting_times = persona.get("content", {}).get("posting_times", ["09:00", "19:00"])
        accounts = persona.get("account_ids", [])
        primary_product = persona.get("primary_product")
        lynk_url = persona.get("lynk_url", "https://lynk.id/jendralbot")

        # Determine media type for this persona
        has_facebook = any(a not in YOUTUBE_ACCTS | INSTAGRAM_ACCTS | TIKTOK_ACCTS for a in accounts)
        # Default: image post (text for facebook/threads engagement, image for IG/TikTok)
        media_type = "image"

        # Build captions using persona voice
        voice = persona.get("voice", {})
        openings = voice.get("signature_openings", ["Check this out:"])
        hashtags = voice.get("hashtags", ["#berkahkarya"])
        random.seed(int(today.replace("-", "")) + hash(persona["persona_id"]) + 1)
        opening = random.choice(openings)
        caption_base = f"{opening}\n\n{headline}\n\n"
        if primary_product:
            caption_base += f"👉 {lynk_url}\n\n"
        caption_base += " ".join(hashtags[:6])

        plan.append({
            "persona_id": persona["persona_id"],
            "display_name": persona["display_name"],
            "niche": niche,
            "headline": headline,
            "caption": caption_base,
            "account_ids": accounts,
            "media_type": media_type,
            "primary_product": primary_product,
            "posting_times": posting_times[:posts_per_day],
            "avatar": persona.get("avatar", {}),
            "date": today,
        })

    plan_file = out_dir / "plan.json"
    plan_file.write_text(json.dumps(plan, indent=2, ensure_ascii=False))
    log.info(f"  ✅ Plan: {len(plan)} persona plans saved → {plan_file}")
    state["phases"]["plan"] = {"status": "done", "file": str(plan_file), "count": len(plan)}
    return state


# ── Phase 3: PRODUCE ──────────────────────────────────────────────────────────
def phase_produce(state: dict) -> dict:
    """Generate visuals for each persona's planned content."""
    log.info("🎨 PHASE 3: PRODUCE")
    today = state["date"]
    out_dir = OUTPUT_DIR / today
    plan_file = out_dir / "plan.json"

    if not plan_file.exists():
        log.warning("  Plan not found, running planning first")
        state = phase_plan(state)

    plan = json.loads(plan_file.read_text())

    try:
        sys.path.insert(0, str(CS_DIR))
        from persona_visual_engine import PersonaVisualEngine
        engine = PersonaVisualEngine()
        use_engine = True
    except Exception as e:
        log.warning(f"  ⚠️  Visual engine unavailable: {e}")
        use_engine = False

    produced = []
    for item in plan:
        persona_id = item["persona_id"]
        headline = item["headline"]
        product = item.get("primary_product", "")
        product_label = product.replace("-", " ").title() if product else None

        if use_engine:
            try:
                img_path = engine.generate_hook_frame(
                    persona_id=persona_id,
                    headline=headline,
                    product_name=product_label,
                )
                item["image_path"] = str(img_path)
                log.info(f"  🖼️  {persona_id}: {img_path.name}")
            except Exception as e:
                log.warning(f"  ⚠️  Image gen failed for {persona_id}: {e}")
                item["image_path"] = None
        else:
            item["image_path"] = None

        produced.append(item)

    produced_file = out_dir / "produced.json"
    produced_file.write_text(json.dumps(produced, indent=2, ensure_ascii=False))
    log.info(f"  ✅ Produced {len(produced)} items → {produced_file}")
    state["phases"]["produce"] = {
        "status": "done", "file": str(produced_file), "count": len(produced),
        "with_image": sum(1 for p in produced if p.get("image_path")),
    }
    return state


# ── Phase 4: REVIEW (Auto-QC) ────────────────────────────────────────────────
def phase_review(state: dict) -> dict:
    """Auto-review: check caption length, media presence, platform compliance."""
    log.info("✅ PHASE 4: REVIEW (Auto-QC)")
    today = state["date"]
    produced_file = OUTPUT_DIR / today / "produced.json"

    if not produced_file.exists():
        log.warning("  Produced items not found, running produce first")
        state = phase_produce(state)

    items = json.loads(produced_file.read_text())
    approved, rejected = [], []

    for item in items:
        issues = []
        caption = item.get("caption", "")
        accounts = item.get("account_ids", [])
        media_type = item.get("media_type")
        img_path = item.get("image_path")

        # Caption checks
        if len(caption) < 20:
            issues.append("Caption too short")
        if len(caption) > 2200:
            issues.append("Caption too long (>2200 chars)")

        # Media compliance
        has_media = img_path and Path(img_path).exists() if img_path else False
        safe_accounts = filter_accounts(accounts, "image" if has_media else None)
        if not safe_accounts:
            issues.append("No compatible accounts after filtering")

        if issues:
            item["review_issues"] = issues
            rejected.append(item)
            log.warning(f"  ❌ {item['persona_id']}: {issues}")
        else:
            item["safe_accounts"] = safe_accounts
            item["reviewed"] = True
            approved.append(item)

    reviewed_file = OUTPUT_DIR / today / "reviewed.json"
    reviewed_file.write_text(json.dumps(approved, indent=2, ensure_ascii=False))
    rejected_file = OUTPUT_DIR / today / "rejected.json"
    rejected_file.write_text(json.dumps(rejected, indent=2, ensure_ascii=False))

    log.info(f"  ✅ Approved: {len(approved)} | Rejected: {len(rejected)}")
    state["phases"]["review"] = {
        "status": "done", "approved": len(approved), "rejected": len(rejected),
    }
    return state


# ── PostBridge helpers ────────────────────────────────────────────────────────
def upload_image_to_postbridge(img_path: str) -> Optional[str]:
    """Upload image, return media_id or None."""
    p = Path(img_path)
    if not p.exists():
        log.warning(f"  Image not found: {img_path}")
        return None
    size = p.stat().st_size
    # Step 1: Get upload URL
    r = requests.post(f"{POSTBRIDGE_API}/media/create-upload-url", headers=PB_HDR, json={
        "name": p.name, "mime_type": "image/png", "size_bytes": size,
    }, timeout=30)
    if r.status_code not in (200, 201):
        log.warning(f"  Upload URL failed {r.status_code}: {r.text[:200]}")
        return None
    data = r.json()
    media_id = data["media_id"]
    upload_url = data["upload_url"]
    # Step 2: PUT file
    with open(p, "rb") as f:
        r2 = requests.put(upload_url, data=f,
                          headers={"Content-Type": "image/png"}, timeout=60)
    if r2.status_code not in (200, 201):
        log.warning(f"  Upload PUT failed {r2.status_code}")
        return None
    return media_id


def schedule_post(caption: str, accounts: list, media_ids: list,
                  scheduled_at: str, platform_configs: dict = None,
                  persona_id: str = None) -> Optional[str]:
    """Create scheduled post, return post_id or None. Queue locally if server error."""
    payload = {
        "caption": caption,
        "social_accounts": accounts,
        "scheduled_at": scheduled_at,
        "media": media_ids if media_ids else None,
    }
    if platform_configs:
        payload["platform_configurations"] = platform_configs
    try:
        r = requests.post(f"{POSTBRIDGE_API}/posts", headers=PB_HDR,
                          json=payload, timeout=30)
        if r.status_code in (200, 201):
            return r.json().get("id")
        elif r.status_code >= 500:
            # Server error — queue for retry
            log.warning(f"  PostBridge 500 error, queueing for retry: {persona_id or 'unknown'}")
            try:
                sys.path.insert(0, str(WORKSPACE / "content_suite"))
                from postbridge_queue_retry import enqueue_post
                enqueue_post(caption, accounts, media_ids, scheduled_at, persona_id)
                return f"QUEUED:{persona_id}"
            except Exception as eq:
                log.error(f"  Queue failed: {eq}")
                return None
        else:
            log.warning(f"  Schedule failed {r.status_code}: {r.text[:300]}")
            return None
    except Exception as e:
        log.error(f"  Schedule exception: {e}")
        return None


# ── Phase 5: PUBLISH ──────────────────────────────────────────────────────────
def phase_publish(state: dict) -> dict:
    """Upload media + schedule posts via PostBridge."""
    log.info("📤 PHASE 5: PUBLISH")
    today = state["date"]
    reviewed_file = OUTPUT_DIR / today / "reviewed.json"

    if not reviewed_file.exists():
        log.warning("  Reviewed items not found, running review first")
        state = phase_review(state)

    items = json.loads(reviewed_file.read_text())
    scheduled, failed = 0, 0
    schedule_log = []

    # Base schedule: spread posts across day
    base_hour = 8  # start at 8 AM
    slot_minutes = 30  # 30 min between posts

    for idx, item in enumerate(items):
        persona_id = item["persona_id"]
        caption = item["caption"]
        accounts = item.get("safe_accounts", item.get("account_ids", []))
        img_path = item.get("image_path")
        posting_times = item.get("posting_times", ["09:00"])
        has_media = img_path and Path(img_path).exists() if img_path else False

        # Upload image if available
        media_ids = []
        if has_media:
            log.info(f"  📎 Uploading image for {persona_id}...")
            media_id = upload_image_to_postbridge(img_path)
            if media_id:
                media_ids.append(media_id)
                log.info(f"    ✅ media_id={media_id}")
            else:
                log.warning(f"    ⚠️  Upload failed, posting text-only (will remove IG/TikTok/YT)")
                # Remove platforms that need media
                accounts = filter_accounts(accounts, None)

        # Filter accounts based on final media state
        final_media_type = "image" if media_ids else None
        final_accounts = filter_accounts(accounts, final_media_type)
        if not final_accounts:
            log.warning(f"  ⏭️  {persona_id}: no compatible accounts, skipping")
            failed += 1
            continue

        # Schedule at persona's preferred times
        for i, post_time in enumerate(posting_times[:2]):
            # Build scheduled_at ISO string for today
            try:
                h, m = map(int, post_time.split(":"))
                scheduled_dt = datetime(
                    int(today[:4]), int(today[5:7]), int(today[8:]),
                    h, m, 0, tzinfo=TZ_JAKARTA
                )
                # If time already passed, schedule tomorrow same time
                now = datetime.now(TZ_JAKARTA)
                if scheduled_dt <= now:
                    scheduled_dt = scheduled_dt + timedelta(days=1)
                scheduled_at = scheduled_dt.strftime("%Y-%m-%dT%H:%M:%S+07:00")
            except Exception:
                # Fallback: 2 hours from now
                scheduled_at = (datetime.now(TZ_JAKARTA) + timedelta(hours=2+i)).strftime("%Y-%m-%dT%H:%M:%S+07:00")

            post_id = schedule_post(
                caption=caption,
                accounts=final_accounts,
                media_ids=media_ids,
                scheduled_at=scheduled_at,
                persona_id=persona_id,
            )
            if post_id:
                if post_id.startswith("QUEUED:"):
                    scheduled += 1  # count queued as scheduled
                    schedule_log.append({
                        "persona_id": persona_id, "post_id": post_id,
                        "scheduled_at": scheduled_at, "accounts": final_accounts,
                        "has_media": bool(media_ids),
                        "status": "queued_postbridge_500",
                    })
                    log.info(f"  📦 {persona_id} queued (PostBridge 500)")
                else:
                    scheduled += 1
                    schedule_log.append({
                        "persona_id": persona_id, "post_id": post_id,
                        "scheduled_at": scheduled_at, "accounts": final_accounts,
                        "has_media": bool(media_ids),
                    })
                    log.info(f"  ✅ {persona_id} @ {scheduled_at} → post_id={post_id}")
            else:
                failed += 1

            time.sleep(0.15)  # Rate limit: max 10 req/sec

    schedule_file = OUTPUT_DIR / today / "schedule_log.json"
    schedule_file.write_text(json.dumps(schedule_log, indent=2, ensure_ascii=False))
    log.info(f"  ✅ Scheduled: {scheduled} | Failed: {failed}")
    state["phases"]["publish"] = {
        "status": "done", "scheduled": scheduled, "failed": failed,
        "file": str(schedule_file),
    }
    state["posts_scheduled"] += scheduled
    return state


# ── Phase 6: ANALYZE ─────────────────────────────────────────────────────────
def phase_analyze(state: dict) -> dict:
    """Sync analytics + generate performance report."""
    log.info("📊 PHASE 6: ANALYZE")
    today = state["date"]
    yesterday = (datetime.strptime(today, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")

    # Trigger analytics sync (TikTok, YouTube, Instagram)
    log.info("  Syncing analytics...")
    for platform in ["tiktok", "youtube", "instagram"]:
        r = requests.post(f"{POSTBRIDGE_API}/analytics/sync?platform={platform}",
                          headers=PB_HDR, timeout=30)
        if r.status_code == 429:
            log.warning(f"  ⚠️  {platform}: rate limited on analytics sync")
        else:
            log.info(f"  ✅ {platform}: sync triggered ({r.status_code})")
        time.sleep(2)

    # Fetch post results for yesterday's posts
    r = requests.get(f"{POSTBRIDGE_API}/post-results?limit=50",
                     headers=PB_HDR, timeout=30)
    results = r.json().get("data", []) if r.status_code == 200 else []

    success = sum(1 for r in results if r.get("success"))
    fail = sum(1 for r in results if not r.get("success"))
    platforms = {}
    for r in results:
        pd = r.get("platform_data", {})
        platform = pd.get("username", "unknown").split("@")[0] if pd else "unknown"

    # Fetch analytics data
    r2 = requests.get(f"{POSTBRIDGE_API}/analytics?limit=20&timeframe=7d",
                      headers=PB_HDR, timeout=30)
    analytics = r2.json().get("data", []) if r2.status_code == 200 else []

    total_views = sum(a.get("view_count", 0) for a in analytics)
    total_likes = sum(a.get("like_count", 0) for a in analytics)
    total_shares = sum(a.get("share_count", 0) for a in analytics)

    report = {
        "date": today,
        "post_results": {"success": success, "fail": fail, "total": len(results)},
        "analytics_7d": {
            "views": total_views, "likes": total_likes, "shares": total_shares,
            "records": len(analytics),
        },
        "success_rate": f"{success/(len(results) or 1)*100:.1f}%",
    }

    report_file = OUTPUT_DIR / today / "analytics_report.json"
    report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    log.info(f"  ✅ Analytics: {total_views} views | {total_likes} likes | {success}/{len(results)} posts OK")
    state["phases"]["analyze"] = {"status": "done", "report": report}
    return state


# ── Main ──────────────────────────────────────────────────────────────────────
def run_all_phases():
    state = load_state()
    phases = [phase_research, phase_plan, phase_produce, phase_review, phase_publish]
    for phase_fn in phases:
        try:
            state = phase_fn(state)
            save_state(state)
        except Exception as e:
            log.error(f"Phase {phase_fn.__name__} failed: {e}", exc_info=True)
            state["errors"].append({"phase": phase_fn.__name__, "error": str(e)})
            save_state(state)
    log.info(f"✅ Pipeline done. Posts scheduled: {state['posts_scheduled']}")
    return state

def show_status():
    state = load_state()
    print(f"\n📊 Pipeline Status — {state['date']}")
    print(f"   Posts scheduled: {state['posts_scheduled']}")
    for phase, info in state.get("phases", {}).items():
        status = info.get("status", "?")
        icon = "✅" if status == "done" else "❌"
        print(f"   {icon} {phase}: {status} — {info}")
    if state.get("errors"):
        print(f"\n❌ Errors: {state['errors']}")


PHASE_MAP = {
    "research": phase_research,
    "plan": phase_plan,
    "produce": phase_produce,
    "review": phase_review,
    "publish": phase_publish,
    "analyze": phase_analyze,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Full Auto Content Pipeline")
    parser.add_argument("--phase", choices=list(PHASE_MAP.keys()), help="Run specific phase")
    parser.add_argument("--all", action="store_true", help="Run all phases")
    parser.add_argument("--status", action="store_true", help="Show today's status")
    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.phase:
        state = load_state()
        state = PHASE_MAP[args.phase](state)
        save_state(state)
        log.info(f"✅ Phase '{args.phase}' complete")
    elif args.all:
        run_all_phases()
    else:
        parser.print_help()
