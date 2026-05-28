"""
Content Kingdom — Learning Engine
==================================
Self-learning module that captures feedback from ALL user interactions,
trainer inputs (Veris, etc.), and content performance data.

Every conversation, every correction, every "ini bagus" or "ini jelek"
gets stored and fed back into future content generation.

Architecture:
  1. CAPTURE — Extract learnings from user messages, trainer feedback, performance data
  2. STORE — Persist to learnings.json (append-only, never lose data)
  3. APPLY — Feed learnings into content generation (captions, images, videos)
  4. EVOLVE — Periodic consolidation of learnings into rules

This makes Content Kingdom a self-improving system.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Learnings database
LEARNINGS_DIR = Path(__file__).parent.parent / "learnings"
LEARNINGS_DB = LEARNINGS_DIR / "learnings.json"
RULES_DB = LEARNINGS_DIR / "rules.json"
TRAINING_LOG = LEARNINGS_DIR / "training_log.json"


def _ensure_dir():
    LEARNINGS_DIR.mkdir(exist_ok=True)


def _load_db(path: Path) -> list:
    _ensure_dir()
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []


def _save_db(path: Path, data):
    _ensure_dir()
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── CAPTURE ──────────────────────────────────────────────

def capture_feedback(
    source: str,
    feedback_type: str,
    content: str,
    context: dict | None = None,
    tags: list | None = None,
):
    """
    Capture ANY feedback from any source.
    
    Args:
        source: Who gave feedback ("user", "veris", "analytics", "system")
        feedback_type: Type of feedback:
            - "positive" — user liked something
            - "negative" — user disliked something  
            - "correction" — user corrected a mistake
            - "instruction" — user gave a new rule/preference
            - "training" — trainer provided design/content guidance
            - "performance" — analytics data (engagement, clicks, sales)
        content: The actual feedback text or data
        context: Optional context (product, platform, post_id, etc.)
        tags: Optional tags for categorization
    
    Returns:
        The stored learning entry
    """
    learnings = _load_db(LEARNINGS_DB)
    
    entry = {
        "id": len(learnings) + 1,
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "type": feedback_type,
        "content": content,
        "context": context or {},
        "tags": tags or [],
        "applied": False,
        "applied_count": 0,
    }
    
    learnings.append(entry)
    _save_db(LEARNINGS_DB, learnings)
    
    # Auto-extract rules from certain feedback types
    if feedback_type in ("instruction", "training", "correction"):
        _auto_extract_rule(entry)
    
    return entry


def capture_trainer_session(
    trainer_name: str,
    principles: list[dict],
    examples: list[dict] | None = None,
):
    """
    Capture a full training session from a human trainer.
    
    Args:
        trainer_name: Name of trainer (e.g., "Veris")
        principles: List of {principle, description, priority}
        examples: Optional list of {description, good_example, bad_example}
    """
    log = _load_db(TRAINING_LOG)
    
    session = {
        "id": len(log) + 1,
        "timestamp": datetime.now().isoformat(),
        "trainer": trainer_name,
        "principles": principles,
        "examples": examples or [],
    }
    
    log.append(session)
    _save_db(TRAINING_LOG, log)
    
    # Convert each principle to a rule
    for p in principles:
        add_rule(
            category=p.get("category", "design"),
            rule=p.get("principle", ""),
            description=p.get("description", ""),
            source=f"trainer:{trainer_name}",
            priority=p.get("priority", 5),
        )
    
    return session


def capture_performance(
    post_id: str,
    platform: str,
    metrics: dict,
    caption_snippet: str = "",
    had_media: bool = False,
    media_type: str = "",
):
    """
    Capture content performance data for learning.
    
    Args:
        post_id: PostBridge post ID
        platform: Platform name (facebook, instagram, etc.)
        metrics: {views, likes, comments, shares, clicks, saves}
        caption_snippet: First 100 chars of caption
        had_media: Whether post had image/video
        media_type: "image", "video", or ""
    """
    return capture_feedback(
        source="analytics",
        feedback_type="performance",
        content=json.dumps(metrics),
        context={
            "post_id": post_id,
            "platform": platform,
            "caption_snippet": caption_snippet,
            "had_media": had_media,
            "media_type": media_type,
        },
        tags=["performance", platform],
    )


# ── STORE (Rules) ───────────────────────────────────────

def add_rule(
    category: str,
    rule: str,
    description: str = "",
    source: str = "user",
    priority: int = 5,
):
    """
    Add or update a content generation rule.
    
    Categories: design, copy, timing, platform, pricing, hook, cta, audience
    Priority: 1 (low) to 10 (critical)
    """
    rules = _load_db(RULES_DB)
    
    # Check if similar rule exists (dedup by rule text)
    for existing in rules:
        if existing["rule"].lower().strip() == rule.lower().strip():
            existing["priority"] = max(existing["priority"], priority)
            existing["updated"] = datetime.now().isoformat()
            existing["sources"].append(source)
            _save_db(RULES_DB, rules)
            return existing
    
    entry = {
        "id": len(rules) + 1,
        "category": category,
        "rule": rule,
        "description": description,
        "sources": [source],
        "priority": priority,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "active": True,
    }
    
    rules.append(entry)
    _save_db(RULES_DB, rules)
    return entry


def _auto_extract_rule(entry: dict):
    """Auto-extract rules from feedback entries."""
    content = entry.get("content", "")
    source = entry.get("source", "user")
    
    # Simple keyword-based rule extraction
    rule_keywords = {
        "design": ["warna", "color", "background", "dark", "font", "layout", "format", "size", "resolution"],
        "copy": ["caption", "hook", "teks", "text", "copy", "headline", "cta"],
        "timing": ["waktu", "jam", "time", "schedule", "posting"],
        "platform": ["instagram", "tiktok", "facebook", "threads", "youtube"],
        "pricing": ["harga", "price", "diskon", "gratis", "free"],
    }
    
    content_lower = content.lower()
    for category, keywords in rule_keywords.items():
        if any(kw in content_lower for kw in keywords):
            add_rule(
                category=category,
                rule=content[:200],
                description=f"Auto-extracted from {entry['type']} feedback",
                source=source,
                priority=6 if entry["type"] == "training" else 4,
            )
            break


# ── APPLY ────────────────────────────────────────────────

def get_active_rules(category: str | None = None) -> list:
    """Get all active rules, optionally filtered by category."""
    rules = _load_db(RULES_DB)
    active = [r for r in rules if r.get("active", True)]
    if category:
        active = [r for r in active if r.get("category") == category]
    return sorted(active, key=lambda r: -r.get("priority", 5))


def get_design_guidelines() -> dict:
    """Get consolidated design guidelines from all learnings."""
    rules = get_active_rules("design")
    
    # Default Veris guidelines (baseline)
    guidelines = {
        "background": "#000000",
        "text_color": "#FFFFFF",
        "accent_trust": "#202040",
        "accent_urgency": "#200000",
        "primary_format": "4:5",
        "primary_platform": "instagram",
        "style": "minimalist_premium",
        "rules": [r["rule"] for r in rules],
    }
    
    return guidelines


def get_copy_guidelines() -> dict:
    """Get consolidated copy/caption guidelines."""
    rules = get_active_rules("copy")
    
    return {
        "tone": "direct, premium, no fluff",
        "language": "bahasa gaul tapi profesional",
        "emoji_policy": "minimal, strategic only",
        "hook_patterns": [
            "Problem agitation → solution",
            "Penyesalan (regret hook)",
            "Rahasia/Bocoran (secret reveal)",
            "Hasil Nyata (proof first)",
            "Kontroversi ringan (mild controversy)",
        ],
        "rules": [r["rule"] for r in rules],
    }


def build_prompt_with_learnings(base_prompt: str, category: str = "design") -> str:
    """Enhance a generation prompt with learned rules."""
    rules = get_active_rules(category)
    
    if not rules:
        return base_prompt
    
    rules_text = "\n".join(f"- {r['rule']}" for r in rules[:10])  # Top 10 by priority
    
    enhanced = f"""{base_prompt}

IMPORTANT RULES (learned from feedback):
{rules_text}"""
    
    return enhanced


def get_top_performing_patterns() -> dict:
    """Analyze performance data to find what works best."""
    learnings = _load_db(LEARNINGS_DB)
    performance = [l for l in learnings if l["type"] == "performance"]
    
    if not performance:
        return {"message": "No performance data yet. Will learn from first posts."}
    
    # Group by platform
    by_platform = {}
    for p in performance:
        ctx = p.get("context", {})
        platform = ctx.get("platform", "unknown")
        metrics = json.loads(p.get("content", "{}"))
        
        if platform not in by_platform:
            by_platform[platform] = {"total": 0, "with_media": 0, "engagement": []}
        
        by_platform[platform]["total"] += 1
        if ctx.get("had_media"):
            by_platform[platform]["with_media"] += 1
        
        eng = sum(metrics.get(k, 0) for k in ["likes", "comments", "shares", "saves"])
        by_platform[platform]["engagement"].append(eng)
    
    # Calculate averages
    result = {}
    for platform, data in by_platform.items():
        avg_eng = sum(data["engagement"]) / len(data["engagement"]) if data["engagement"] else 0
        result[platform] = {
            "total_posts": data["total"],
            "media_rate": data["with_media"] / data["total"] if data["total"] else 0,
            "avg_engagement": round(avg_eng, 1),
        }
    
    return result


# ── EVOLVE ───────────────────────────────────────────────

def get_learning_stats() -> dict:
    """Get stats about the learning system."""
    learnings = _load_db(LEARNINGS_DB)
    rules = _load_db(RULES_DB)
    training = _load_db(TRAINING_LOG)
    
    by_type = {}
    for l in learnings:
        t = l.get("type", "?")
        by_type[t] = by_type.get(t, 0) + 1
    
    by_source = {}
    for l in learnings:
        s = l.get("source", "?")
        by_source[s] = by_source.get(s, 0) + 1
    
    return {
        "total_learnings": len(learnings),
        "total_rules": len(rules),
        "active_rules": sum(1 for r in rules if r.get("active", True)),
        "training_sessions": len(training),
        "by_type": by_type,
        "by_source": by_source,
    }


# ── BOOTSTRAP: Load Veris Training ──────────────────────

def bootstrap_veris():
    """Bootstrap with Veris's training data (run once)."""
    rules = _load_db(RULES_DB)
    if any(r.get("sources", [None])[0] == "trainer:Veris" for r in rules):
        return "Already bootstrapped"
    
    capture_trainer_session(
        trainer_name="Veris",
        principles=[
            {
                "category": "design",
                "principle": "Dark background (#000000) for all content images",
                "description": "Pure black creates high contrast, premium feel. 8/10 Veris samples use #000000.",
                "priority": 9,
            },
            {
                "category": "design",
                "principle": "4:5 vertical format (1024x1280) as primary, 1:1 as secondary",
                "description": "70% of Veris samples use 4:5. Better for IG portrait/story. More space for text.",
                "priority": 9,
            },
            {
                "category": "design",
                "principle": "Three-section layout: Hook (top 20-30%) → Body (middle 40-50%) → CTA (bottom 20-30%)",
                "description": "Consistent across all Veris samples. CTA in bordered box at bottom.",
                "priority": 8,
            },
            {
                "category": "design",
                "principle": "No vibrant colors. Subtle accents only: blue #202040, red #200000, gray #606080",
                "description": "Veris avoids overwhelming colors. Focus on content over decoration.",
                "priority": 8,
            },
            {
                "category": "design",
                "principle": "White text on black background. Clean modern sans-serif. Readable at 320px mobile width",
                "description": "Maximum readability. Bold for hooks, regular for body.",
                "priority": 8,
            },
            {
                "category": "platform",
                "principle": "Instagram-first strategy. Not TikTok-first.",
                "description": "Veris optimizes for IG conversion. TikTok is volume play, not primary.",
                "priority": 7,
            },
            {
                "category": "design",
                "principle": "Minimalist premium aesthetic. No emoji in images. No complex patterns/gradients.",
                "description": "Clean backgrounds, text as primary visual element.",
                "priority": 7,
            },
            {
                "category": "copy",
                "principle": "Direct, premium tone. No fluff. Every word must earn its place.",
                "description": "Veris copy is concise, authoritative, action-oriented.",
                "priority": 7,
            },
        ],
        examples=[
            {
                "description": "Background style",
                "good_example": "Pure black #000000 with white text",
                "bad_example": "Purple-pink gradient with colorful emoji",
            },
            {
                "description": "Format choice",
                "good_example": "4:5 vertical (1024x1280) for Instagram",
                "bad_example": "9:16 for TikTok as default",
            },
        ],
    )
    
    return "Veris training bootstrapped: 8 principles, 2 examples"
