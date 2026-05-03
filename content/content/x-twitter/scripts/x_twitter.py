#!/usr/bin/env python3
"""
x_twitter.py — Python wrapper for the `twitter` CLI tool.

Uses TWITTER_AUTH_TOKEN and TWITTER_CT0 from environment (loaded via ~/.bashrc).
Shells out to the `twitter` CLI at /home/openclaw/.local/bin/twitter.
"""

import subprocess
import shutil
import sys
import argparse
import json
import os

# Resolve which CLI binary to use: prefer `twitter`, fall back to `twclaw`
TWITTER_BIN = "/home/openclaw/.local/bin/twitter"
if not os.path.isfile(TWITTER_BIN):
    _twclaw = shutil.which("twclaw")
    if _twclaw:
        TWITTER_BIN = _twclaw
    else:
        print("ERROR: neither 'twitter' nor 'twclaw' CLI found.", file=sys.stderr)
        sys.exit(1)


def _run(args: list[str], json_output: bool = True) -> str:
    """Run a twitter CLI command and return its stdout."""
    cmd = [TWITTER_BIN] + args
    if json_output:
        cmd.append("--json")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        err = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"twitter CLI error (exit {result.returncode}): {err}")
    return result.stdout.strip()


def _run_json(args: list[str]) -> dict | list | str:
    """Run a twitter CLI command and parse JSON output."""
    raw = _run(args, json_output=True)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


# ── Public API ───────────────────────────────────────────────────────────────

def post(text: str) -> dict | str:
    """Post a tweet."""
    return _run_json(["post", text])


def reply(tweet_id: str, text: str) -> dict | str:
    """Reply to a tweet."""
    return _run_json(["reply", str(tweet_id), text])


def search(query: str, n: int = 10) -> dict | list | str:
    """Search tweets."""
    return _run_json(["search", query, "-n", str(n)])


def get_tweet(tweet_id: str) -> dict | str:
    """Get a single tweet by ID."""
    return _run_json(["tweet", str(tweet_id)])


def timeline(n: int = 20) -> dict | list | str:
    """Get home timeline (following feed)."""
    return _run_json(["feed", "-t", "following", "-n", str(n)])


def user(username: str) -> dict | str:
    """Get user profile info."""
    return _run_json(["user", username])


def like(tweet_id: str) -> dict | str:
    """Like a tweet."""
    return _run_json(["like", str(tweet_id)])


def retweet(tweet_id: str) -> dict | str:
    """Retweet a tweet."""
    return _run_json(["retweet", str(tweet_id)])


# ── CLI Interface ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="X/Twitter CLI wrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # post
    p_post = sub.add_parser("post", help="Post a tweet")
    p_post.add_argument("text", help="Tweet text")

    # reply
    p_reply = sub.add_parser("reply", help="Reply to a tweet")
    p_reply.add_argument("tweet_id", help="Tweet ID to reply to")
    p_reply.add_argument("text", help="Reply text")

    # search
    p_search = sub.add_parser("search", help="Search tweets")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--count", "-n", type=int, default=10, help="Number of results")

    # get
    p_get = sub.add_parser("get", help="Get a tweet by ID")
    p_get.add_argument("tweet_id", help="Tweet ID")

    # timeline
    p_tl = sub.add_parser("timeline", help="Get home timeline")
    p_tl.add_argument("--count", "-n", type=int, default=20, help="Number of tweets")

    # user
    p_user = sub.add_parser("user", help="Get user info")
    p_user.add_argument("username", help="Username (without @)")

    # like
    p_like = sub.add_parser("like", help="Like a tweet")
    p_like.add_argument("tweet_id", help="Tweet ID")

    # retweet
    p_rt = sub.add_parser("retweet", help="Retweet a tweet")
    p_rt.add_argument("tweet_id", help="Tweet ID")

    args = parser.parse_args()

    try:
        if args.command == "post":
            result = post(args.text)
        elif args.command == "reply":
            result = reply(args.tweet_id, args.text)
        elif args.command == "search":
            result = search(args.query, n=args.count)
        elif args.command == "get":
            result = get_tweet(args.tweet_id)
        elif args.command == "timeline":
            result = timeline(n=args.count)
        elif args.command == "user":
            result = user(args.username)
        elif args.command == "like":
            result = like(args.tweet_id)
        elif args.command == "retweet":
            result = retweet(args.tweet_id)
        else:
            parser.print_help()
            sys.exit(1)

        if isinstance(result, (dict, list)):
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(result)

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
