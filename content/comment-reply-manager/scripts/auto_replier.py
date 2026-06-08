"""
auto_replier.py — Orchestrate comment replies with contextual responses
Combines sentiment analysis, FAQ matching, and template selection
"""

import json
import os
import time
from datetime import datetime
from typing import Optional

from sentiment_analyzer import analyze_sentiment, SentimentResult
from faq_responder import find_faq_response
from comment_templates import (
    get_positive_reply,
    get_question_reply,
    get_interest_reply,
    get_negative_reply,
    get_price_reply,
    get_dm_public_reply,
    get_generic_reply,
    find_product_by_keywords,
    PRODUCTS,
)

# ─── CONFIG ────────────────────────────────────────────────────────────────────
REPLY_LOG_FILE = os.path.expanduser(
    "~/.openclaw/workspace/skills/1ai-skills/content/comment-reply-manager/logs/replies.jsonl"
)
REPLIED_IDS_FILE = os.path.expanduser(
    "~/.openclaw/workspace/skills/1ai-skills/content/comment-reply-manager/cache/replied_ids.json"
)

# Cooldown between replies (seconds) — avoid rate limits
REPLY_DELAY_SECONDS = 2.0

# ─── REPLY DECISION ENGINE ─────────────────────────────────────────────────────


class ReplyDecision:
    def __init__(
        self, comment: dict, reply_text: str, should_dm: bool, dm_product: dict = None
    ):
        self.comment = comment
        self.reply_text = reply_text
        self.should_dm = should_dm
        self.dm_product = dm_product
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "comment_id": self.comment.get("id"),
            "platform": self.comment.get("platform"),
            "username": self.comment.get("username"),
            "comment_text": self.comment.get("text", "")[:200],
            "reply_text": self.reply_text,
            "should_dm": self.should_dm,
            "dm_product": self.dm_product["name"] if self.dm_product else None,
        }


def decide_reply(comment: dict) -> ReplyDecision:
    """
    Core logic: Given a comment dict, decide what to reply.
    comment dict: {id, platform, username, text, post_id, post_caption}
    """
    text = comment.get("text", "")
    post_caption = comment.get("post_caption", "")

    # 1. Sentiment analysis
    sentiment: SentimentResult = analyze_sentiment(text)

    # Skip spam entirely
    if sentiment.category == "spam":
        return ReplyDecision(
            comment=comment,
            reply_text="[SKIP - SPAM]",
            should_dm=False,
        )

    # 2. Find relevant product based on comment + post context
    combined_text = f"{text} {post_caption}"
    product = find_product_by_keywords(combined_text)

    # 3. Try FAQ first (highest priority — specific answers)
    faq_response = find_faq_response(text)
    if faq_response:
        return ReplyDecision(
            comment=comment,
            reply_text=faq_response,
            should_dm=sentiment.is_dm_trigger,
            dm_product=product if sentiment.is_dm_trigger else None,
        )

    # 4. Route by sentiment category
    if sentiment.category == "price_ask":
        reply = get_price_reply(product)
        return ReplyDecision(
            comment=comment,
            reply_text=reply,
            should_dm=True,  # Price ask = strong buyer signal → DM
            dm_product=product,
        )

    elif sentiment.category == "interest":
        reply = get_dm_public_reply()  # "DM ya kak buat detail!"
        return ReplyDecision(
            comment=comment,
            reply_text=reply,
            should_dm=True,
            dm_product=product,
        )

    elif sentiment.category == "question":
        reply = get_question_reply(product)
        return ReplyDecision(
            comment=comment,
            reply_text=reply,
            should_dm=sentiment.is_dm_trigger,
            dm_product=product if sentiment.is_dm_trigger else None,
        )

    elif sentiment.category == "positive":
        reply = get_positive_reply()
        return ReplyDecision(
            comment=comment,
            reply_text=reply,
            should_dm=False,
        )

    elif sentiment.category == "negative":
        reply = get_negative_reply()
        return ReplyDecision(
            comment=comment,
            reply_text=reply,
            should_dm=False,
        )

    else:  # neutral
        reply = get_generic_reply()
        return ReplyDecision(
            comment=comment,
            reply_text=reply,
            should_dm=False,
        )


# ─── REPLY TRACKING ────────────────────────────────────────────────────────────


def load_replied_ids() -> set:
    if not os.path.exists(REPLIED_IDS_FILE):
        return set()
    with open(REPLIED_IDS_FILE) as f:
        data = json.load(f)
    return set(data.get("ids", []))


def save_replied_ids(ids: set):
    os.makedirs(os.path.dirname(REPLIED_IDS_FILE), exist_ok=True)
    with open(REPLIED_IDS_FILE, "w") as f:
        json.dump({"ids": list(ids), "updated_at": datetime.now().isoformat()}, f)


def log_reply(decision: ReplyDecision):
    os.makedirs(os.path.dirname(REPLY_LOG_FILE), exist_ok=True)
    with open(REPLY_LOG_FILE, "a") as f:
        f.write(json.dumps(decision.to_dict()) + "\n")


def already_replied(comment_id: str, replied_ids: set) -> bool:
    return comment_id in replied_ids


# ─── PLATFORM REPLY DISPATCHER ─────────────────────────────────────────────────


def reply_to_comment_tiktok(comment: dict, reply_text: str) -> bool:
    """
    Reply to TikTok comment.
    NOTE: TikTok's official API doesn't support posting comments via v2 API.
    Use browser automation as fallback.
    Returns True on success.
    """
    print(f"[TikTok] Would reply to @{comment.get('username')}: {reply_text[:60]}...")
    # TODO: Implement via browser automation (see auto_replier_browser.py)
    # For now: log to manual action queue
    log_manual_action(comment, reply_text, "tiktok")
    return False  # Not auto-implemented yet


def reply_to_comment_instagram(comment: dict, reply_text: str) -> bool:
    """
    Reply to Instagram comment via Instagram Graph API (if token available).
    Returns True on success.
    """
    print(
        f"[Instagram] Would reply to @{comment.get('username')}: {reply_text[:60]}..."
    )
    log_manual_action(comment, reply_text, "instagram")
    return False  # Requires IG access token


def reply_to_comment(comment: dict, reply_text: str) -> bool:
    """Dispatch reply to appropriate platform handler."""
    platform = comment.get("platform", "unknown").lower()
    if platform == "tiktok":
        return reply_to_comment_tiktok(comment, reply_text)
    elif platform in ("instagram", "ig"):
        return reply_to_comment_instagram(comment, reply_text)
    else:
        print(f"[AutoReplier] Unknown platform: {platform}")
        return False


MANUAL_QUEUE_FILE = os.path.expanduser(
    "~/.openclaw/workspace/skills/1ai-skills/content/comment-reply-manager/logs/manual_queue.jsonl"
)


def log_manual_action(comment: dict, reply_text: str, platform: str):
    """Log action to manual queue for human to execute."""
    os.makedirs(os.path.dirname(MANUAL_QUEUE_FILE), exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": "reply",
        "platform": platform,
        "post_url": comment.get("post_url", ""),
        "comment_id": comment.get("id"),
        "commenter": comment.get("username"),
        "original_comment": comment.get("text", "")[:200],
        "suggested_reply": reply_text,
        "status": "pending",
    }
    with open(MANUAL_QUEUE_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ─── MAIN PROCESSOR ────────────────────────────────────────────────────────────


def process_comments(comments: list, dry_run: bool = True) -> dict:
    """
    Process list of comments. Returns summary stats.
    dry_run=True: log decisions but don't actually post replies
    """
    replied_ids = load_replied_ids()
    stats = {
        "total": len(comments),
        "skipped_already_replied": 0,
        "skipped_spam": 0,
        "replied": 0,
        "dm_triggers": 0,
        "errors": 0,
    }

    for comment in comments:
        comment_id = comment.get("id", "")

        # Skip already-replied
        if already_replied(comment_id, replied_ids):
            stats["skipped_already_replied"] += 1
            continue

        # Decide reply
        decision = decide_reply(comment)

        # Skip spam
        if "[SKIP" in decision.reply_text:
            stats["skipped_spam"] += 1
            log_reply(decision)
            continue

        print(f"\n[AutoReplier] Comment: '{comment.get('text', '')[:60]}'")
        print(f"              Reply:   '{decision.reply_text[:60]}'")
        print(f"              DM:      {decision.should_dm}")

        if not dry_run:
            success = reply_to_comment(comment, decision.reply_text)
            if success:
                replied_ids.add(comment_id)
                stats["replied"] += 1
            else:
                stats["errors"] += 1
        else:
            # Dry run: just log
            stats["replied"] += 1

        if decision.should_dm:
            stats["dm_triggers"] += 1

        log_reply(decision)
        time.sleep(REPLY_DELAY_SECONDS)

    save_replied_ids(replied_ids)
    return stats


if __name__ == "__main__":
    # Test with sample comments
    sample_comments = [
        {
            "id": "1",
            "platform": "tiktok",
            "username": "user_a",
            "text": "Kak harganya berapa?",
            "post_caption": "AI Tools",
        },
        {
            "id": "2",
            "platform": "tiktok",
            "username": "user_b",
            "text": "Mantap banget nih!",
            "post_caption": "AI Tools",
        },
        {
            "id": "3",
            "platform": "instagram",
            "username": "user_c",
            "text": "Mau dong, cara belinya gimana?",
            "post_caption": "JobMagnet",
        },
        {
            "id": "4",
            "platform": "tiktok",
            "username": "user_d",
            "text": "Scam! Penipuan!",
            "post_caption": "AI",
        },
        {
            "id": "5",
            "platform": "tiktok",
            "username": "user_e",
            "text": "Ini bisa buat apa ya?",
            "post_caption": "AI Studio",
        },
        {
            "id": "6",
            "platform": "tiktok",
            "username": "user_f",
            "text": "Follow back dong!",
            "post_caption": "",
        },
        {
            "id": "7",
            "platform": "tiktok",
            "username": "user_g",
            "text": "Pengen coba TikTok affiliate",
            "post_caption": "",
        },
    ]

    print("=== Auto Replier Test (DRY RUN) ===\n")
    stats = process_comments(sample_comments, dry_run=True)
    print(f"\n=== STATS ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
