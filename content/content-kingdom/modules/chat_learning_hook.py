"""
Content Kingdom — Chat Learning Hook
=====================================
Intercepts user messages to extract content-related learnings.
Called by the main agent whenever a user provides feedback about content.

Usage from agent:
    from skills.content_kingdom.modules.chat_learning_hook import process_user_feedback
    process_user_feedback(user_message, user_name="Paijo")

This is the "self-learning" bridge between conversations and Content Kingdom.
"""

import re
from typing import Optional
from . import learning_engine as le


# Keywords that indicate content-related feedback
CONTENT_SIGNALS = {
    "positive": [
        "bagus", "mantap", "keren", "suka", "nice", "good", "perfect",
        "oke", "ok", "bener", "betul", "setuju", "approve", "yes",
        "viral", "rame", "engage", "laku", "convert", "sold",
    ],
    "negative": [
        "jelek", "buruk", "ganti", "ubah", "salah", "wrong", "bad",
        "spam", "sampah", "jangan", "stop", "hapus", "delete",
        "ga cocok", "ga match", "ga suka", "norak", "lebay",
    ],
    "instruction": [
        "harus", "wajib", "selalu", "jangan pernah", "rules", "rule",
        "pakai", "gunakan", "format", "template", "style",
        "mulai sekarang", "dari sekarang", "ingat", "remember",
    ],
    "design": [
        "warna", "color", "background", "font", "layout", "gambar",
        "image", "foto", "dark", "light", "size", "resolusi",
        "vertical", "horizontal", "ratio", "format",
    ],
    "copy": [
        "caption", "hook", "teks", "text", "copy", "headline",
        "cta", "judul", "title", "deskripsi", "description",
        "bahasa", "tone", "gaya", "emoji",
    ],
}


def detect_feedback_type(message: str) -> Optional[str]:
    """Detect what kind of content feedback this message contains."""
    msg_lower = message.lower()
    
    scores = {}
    for ftype, keywords in CONTENT_SIGNALS.items():
        score = sum(1 for kw in keywords if kw in msg_lower)
        if score > 0:
            scores[ftype] = score
    
    if not scores:
        return None
    
    return max(scores, key=scores.get)


def extract_content_context(message: str) -> dict:
    """Extract context about what content element is being discussed."""
    msg_lower = message.lower()
    context = {}
    
    # Detect platform references
    platforms = {
        "tiktok": ["tiktok", "tt", "fyp"],
        "instagram": ["instagram", "ig", "insta", "reels"],
        "facebook": ["facebook", "fb"],
        "youtube": ["youtube", "yt", "shorts"],
        "threads": ["threads"],
    }
    for platform, keywords in platforms.items():
        if any(kw in msg_lower for kw in keywords):
            context["platform"] = platform
            break
    
    # Detect content type references
    content_types = {
        "image": ["gambar", "image", "foto", "photo", "visual"],
        "video": ["video", "clip", "reel", "short"],
        "caption": ["caption", "teks", "text", "copy", "hook"],
        "design": ["design", "layout", "template", "warna", "color"],
    }
    for ctype, keywords in content_types.items():
        if any(kw in msg_lower for kw in keywords):
            context["content_type"] = ctype
            break
    
    # Detect product references
    products = {
        "sellpix": ["sellpix", "marketplace"],
        "guru_pintar": ["guru", "teacher", "pendidik"],
        "mesin_cetak": ["kuliner", "food", "restaurant"],
        "jobmagnet": ["job", "kerja", "cv", "lamaran"],
        "creative_tools": ["creative", "kreatif", "konten"],
        "ad_engine": ["iklan", "ads", "advertising"],
    }
    for product, keywords in products.items():
        if any(kw in msg_lower for kw in keywords):
            context["product"] = product
            break
    
    return context


def process_user_feedback(
    message: str,
    user_name: str = "user",
    user_role: str = "user",
) -> Optional[dict]:
    """
    Process a user message for content-related learnings.
    
    Call this from the main agent on EVERY user message.
    Returns the stored learning entry, or None if message
    has no content-related feedback.
    
    Args:
        message: Raw user message text
        user_name: Name of the user (for attribution)
        user_role: "user", "trainer", "admin"
    """
    feedback_type = detect_feedback_type(message)
    
    if not feedback_type:
        return None  # Not content-related
    
    context = extract_content_context(message)
    context["user"] = user_name
    context["role"] = user_role
    
    # Determine source based on known trainers
    source = "user"
    if user_name.lower() in ("veris", "andik veris", "alwayscuanbos"):
        source = "trainer:Veris"
        if feedback_type in ("positive", "negative"):
            feedback_type = "training"  # Veris feedback is always training-grade
    
    # Map feedback types
    type_map = {
        "positive": "positive",
        "negative": "negative",
        "instruction": "instruction",
        "design": "training",
        "copy": "training",
    }
    
    stored_type = type_map.get(feedback_type, feedback_type)
    
    tags = [feedback_type]
    if context.get("platform"):
        tags.append(context["platform"])
    if context.get("content_type"):
        tags.append(context["content_type"])
    
    return le.capture_feedback(
        source=source,
        feedback_type=stored_type,
        content=message,
        context=context,
        tags=tags,
    )


def process_trainer_input(
    trainer_name: str,
    message: str,
    media_urls: list = None,
) -> dict:
    """
    Process input from a known trainer (like Veris).
    Trainers get elevated priority in the learning system.
    
    This should be called when we detect messages from
    known trainer Telegram accounts.
    """
    context = extract_content_context(message)
    context["trainer"] = trainer_name
    if media_urls:
        context["media_urls"] = media_urls
    
    return le.capture_feedback(
        source=f"trainer:{trainer_name}",
        feedback_type="training",
        content=message,
        context=context,
        tags=["training", trainer_name.lower()],
    )


# Trainer registry — add new trainers here
KNOWN_TRAINERS = {
    "157228659": {"name": "Veris", "username": "alwayscuanbos", "role": "ads_master"},
    "228956686": {"name": "Paijo", "username": "Oyi77", "role": "admin"},
    "5220170786": {"name": "Paijo", "username": "codergaboets", "role": "admin"},
}


def is_known_trainer(sender_id: str) -> Optional[dict]:
    """Check if a sender is a known trainer."""
    return KNOWN_TRAINERS.get(str(sender_id))
