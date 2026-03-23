#!/usr/bin/env python3
"""
Eddie Agent — BerkahKarya Content Publishing Engine
Main entry point for cron execution.

Modes:
  --mode post       Generate and publish 1 post per platform
  --mode report     Generate KPI report (last 7 days)
  --mode all        Post + report (default)
  --mode dry-run    Post simulation, no actual API calls

Usage:
  python3 skills/eddie-agent/eddie.py --mode all
  python3 skills/eddie-agent/eddie.py --mode post
  python3 skills/eddie-agent/eddie.py --mode report
  python3 skills/eddie-agent/eddie.py --mode dry-run
"""

import argparse
import json
import logging
import logging.handlers
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent
MODULES_DIR = SKILL_DIR / "modules"
sys.path.insert(0, str(MODULES_DIR))

from postbridge import get_client_from_config
from content_generator import ContentGenerator
from kpi_reporter import KPIReporter


def setup_logging(config: dict) -> logging.Logger:
    """Configure rotating file + stdout logging."""
    log_cfg = config.get("logging", {})
    log_dir = Path(log_cfg.get("log_dir", str(SKILL_DIR / "logs")))
    log_dir.mkdir(parents=True, exist_ok=True)

    level = getattr(logging, log_cfg.get("level", "INFO").upper(), logging.INFO)
    logger = logging.getLogger("eddie")
    logger.setLevel(level)

    if not logger.handlers:
        # Rotating file handler
        fh = logging.handlers.RotatingFileHandler(
            log_dir / "eddie_agent.log",
            maxBytes=log_cfg.get("max_bytes", 5 * 1024 * 1024),
            backupCount=log_cfg.get("backup_count", 5),
            encoding="utf-8"
        )
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s — %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        logger.addHandler(fh)

        # Stdout handler
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(level)
        sh.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s — %(message)s",
                                          datefmt="%H:%M:%S"))
        logger.addHandler(sh)

    return logger


def load_config() -> dict:
    config_path = SKILL_DIR / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_post(config: dict, logger: logging.Logger, dry_run: bool = False) -> int:
    """
    Generate and publish posts to all active platforms.
    Returns count of successful posts.
    """
    pb = get_client_from_config(config)
    generator = ContentGenerator(config, pb)

    accounts_cfg = config.get("accounts", {})
    posts_per_run = config.get("content", {}).get("posts_per_run", 1)
    platforms_needing_media = set(config.get("content", {}).get("platforms_requiring_media", ["tiktok", "instagram"]))

    logger.info(f"=== Eddie POST run | dry_run={dry_run} | {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")

    # Build platform → account_ids map
    platform_accounts = {}
    for platform, accts in accounts_cfg.items():
        active = [str(a["id"]) for a in accts if a.get("active", True)]
        if active:
            platform_accounts[platform] = active

    logger.info(f"Active platforms: {list(platform_accounts.keys())}")

    success_count = 0
    fail_count = 0

    for platform, account_ids in platform_accounts.items():
        for _ in range(posts_per_run):
            try:
                # Generate post (includes media upload for TikTok/IG)
                post = generator.generate_post(
                    platform=platform,
                    dry_run=dry_run
                )
                product = post["product"]

                if not post["ready"]:
                    logger.warning(f"Post not ready for {platform} (product={product['id']}) — skipping")
                    fail_count += 1
                    continue

                caption = post["caption"]
                media_id = post.get("media_id")

                if dry_run:
                    logger.info(
                        f"[DRY RUN] Would post to {platform} | product={product['id']} | "
                        f"accounts={account_ids} | media={media_id or 'none'}"
                    )
                    logger.info(f"  Caption preview: {caption[:80]}...")
                    success_count += 1
                    continue

                # Publish
                media_ids = [media_id] if media_id else None
                resp = pb.create_post(
                    caption=caption,
                    social_account_ids=account_ids,
                    media_ids=media_ids
                )

                post_id = resp.get("id") or resp.get("data", {}).get("id", "unknown")
                logger.info(
                    f"✅ Posted to {platform} | product={product['id']} | "
                    f"accounts={len(account_ids)} | post_id={post_id}"
                )
                success_count += 1

            except Exception as e:
                logger.error(f"❌ Failed to post on {platform}: {e}", exc_info=True)
                fail_count += 1

    logger.info(f"POST run complete — success={success_count}, failed={fail_count}")
    return success_count


def run_report(config: dict, logger: logging.Logger) -> str:
    """Generate and log KPI report. Returns report path."""
    pb = get_client_from_config(config)
    reporter = KPIReporter(config, pb)

    logger.info("=== Eddie REPORT run ===")
    report_md = reporter.generate_report(days_back=7, save=True)

    # Log first 10 lines to stdout
    lines = report_md.strip().split("\n")
    for line in lines[:15]:
        logger.info(line)

    logger.info("KPI report generated successfully")
    return report_md


def main():
    parser = argparse.ArgumentParser(description="Eddie Agent — BerkahKarya Content Publisher")
    parser.add_argument(
        "--mode",
        choices=["post", "report", "all", "dry-run"],
        default="all",
        help="Execution mode (default: all)"
    )
    args = parser.parse_args()

    config = load_config()
    logger = setup_logging(config)

    logger.info(f"🚀 Eddie Agent starting | mode={args.mode}")

    try:
        if args.mode == "post":
            run_post(config, logger, dry_run=False)

        elif args.mode == "report":
            run_report(config, logger)

        elif args.mode == "all":
            run_post(config, logger, dry_run=False)
            run_report(config, logger)

        elif args.mode == "dry-run":
            run_post(config, logger, dry_run=True)

        logger.info(f"✅ Eddie Agent done | mode={args.mode}")
        sys.exit(0)

    except Exception as e:
        logger.error(f"💥 Eddie Agent crashed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
