#!/usr/bin/env python3
"""
halo-announce — Post announcements to the halo-ai Discord channel.

Usage:
    halo-announce "Your announcement message here"
    halo-announce --channel 123456789 "Message to specific channel"
    echo "message" | halo-announce --stdin

Environment:
    DISCORD_WEBHOOK_URL  — Discord webhook URL (no bot token needed)
"""

import sys
import os
import json
import urllib.request
import urllib.error
import argparse
from datetime import datetime

CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
DIM = "\033[2m"
BOLD = "\033[1m"
NC = "\033[0m"

def announce(message: str, webhook_url: str, username: str = "Halo AI") -> bool:
    """Post a message to Discord via webhook. No bot token needed."""
    payload = json.dumps({
        "username": username,
        "content": message,
    }).encode()

    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.status == 204
    except urllib.error.HTTPError as e:
        print(f"  {RED} x{NC} Discord returned {e.code}: {e.read().decode()}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  {RED} x{NC} Failed: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Post announcements to halo-ai Discord")
    parser.add_argument("message", nargs="?", help="The announcement message")
    parser.add_argument("--stdin", action="store_true", help="Read message from stdin")
    parser.add_argument("--webhook", help="Discord webhook URL (or set DISCORD_WEBHOOK_URL)")
    parser.add_argument("--name", default="Halo AI", help="Bot display name (default: Halo AI)")
    parser.add_argument("--quiet", action="store_true", help="No output on success")
    args = parser.parse_args()

    # Get message
    if args.stdin:
        message = sys.stdin.read().strip()
    elif args.message:
        message = args.message
    else:
        parser.error("Provide a message or use --stdin")

    if not message:
        parser.error("Message cannot be empty")

    # Get webhook URL
    webhook_url = args.webhook or os.environ.get("DISCORD_WEBHOOK_URL", "")
    if not webhook_url:
        print(f"  {RED} x{NC} No webhook URL. Set DISCORD_WEBHOOK_URL or use --webhook")
        print()
        print(f"  {DIM}To create a webhook:{NC}")
        print(f"  {DIM}1. Open your Discord server{NC}")
        print(f"  {DIM}2. Server Settings > Integrations > Webhooks > New Webhook{NC}")
        print(f"  {DIM}3. Pick the announcements channel{NC}")
        print(f"  {DIM}4. Copy the webhook URL{NC}")
        print(f"  {DIM}5. export DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...'{NC}")
        sys.exit(1)

    # Post
    if not args.quiet:
        print(f"  {CYAN}>>>{NC} Posting to Discord as {BOLD}{args.name}{NC}...")

    if announce(message, webhook_url, args.name):
        if not args.quiet:
            print(f"  {GREEN} +{NC} Announced: {message[:80]}{'...' if len(message) > 80 else ''}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
