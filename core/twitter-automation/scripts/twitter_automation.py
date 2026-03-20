#!/usr/bin/env python3
"""Twitter/X Automation wrapper for twitter-cli"""
import subprocess, json, sys, os
from pathlib import Path


def run_twitter(args):
    env = {
        **os.environ,
        "TWITTER_AUTH_TOKEN": os.environ.get("TWITTER_AUTH_TOKEN", ""),
        "TWITTER_CT0": os.environ.get("TWITTER_CT0", ""),
    }
    result = subprocess.run(
        ["twitter"] + args + ["--yaml"],
        capture_output=True,
        text=True,
        env=env,
    )
    return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"


def post_tweet(text):
    return run_twitter(["post", text])


def reply_tweet(tweet_id, text):
    return run_twitter(["reply", tweet_id, text])


def search_tweets(query, limit=10):
    return run_twitter(["search", query, "-n", str(limit)])


def get_tweet(tweet_id):
    return run_twitter(["tweet", tweet_id])


def get_timeline():
    return run_twitter(["feed"])


def get_user(username):
    return run_twitter(["user", username])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Twitter/X Automation CLI")
    parser.add_argument(
        "--action",
        choices=["post", "reply", "search", "tweet", "feed", "user"],
        required=True,
    )
    parser.add_argument("--text", help="Tweet text or search query")
    parser.add_argument("--id", help="Tweet ID for reply/get")
    parser.add_argument("--username", help="Username for user lookup")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if args.action == "post":
        print(post_tweet(args.text))
    elif args.action == "reply":
        print(reply_tweet(args.id, args.text))
    elif args.action == "search":
        print(search_tweets(args.text, args.limit))
    elif args.action == "tweet":
        print(get_tweet(args.id))
    elif args.action == "feed":
        print(get_timeline())
    elif args.action == "user":
        print(get_user(args.username))
