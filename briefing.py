#!/usr/bin/env python3
"""ShaneBrain Daily Briefing — 6am push notification system."""

import subprocess
import sys
import json
import os
import random
from datetime import date, datetime, timezone

SOBRIETY_START = date(2023, 11, 27)
BRIEFING_LOG_DIR = "/mnt/shanebrain-raid/shanebrain-core/briefings"
NTFY_TOPIC = "shanebrain-briefing"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

MOTIVATIONAL_LINES = [
    "You built a Pi cluster from scratch. Today is nothing.",
    "Tiffany needs you sharp. Stay sharp.",
    "Your drivers are counting on you. So is Gavin.",
    "You have been clean since November 2023. That is not small. Keep going.",
    "SRM, Angel Cloud, the book, the cluster — you built all of it. Own today.",
    "Dispatch is the spine of the operation. You are the spine. Hold.",
    "You do not need permission to have a good day. Go have one.",
    "The boys are watching how you handle hard days. Show them.",
    "Every system running right now runs because you built it. Do not forget that.",
    "Hard mornings are just mornings. You have had worse. Move.",
]


def get_weather():
    try:
        result = subprocess.run(
            ["curl", "-s", "wttr.in/Hazel+Green+AL?format=3"],
            capture_output=True, text=True, timeout=10
        )
        line = result.stdout.strip()
        if line:
            return f"Weather: {line}"
    except Exception:
        pass
    return "Weather: Unable to fetch — check weather.com for Hazel Green AL"


def get_sobriety():
    today = date.today()
    delta = today - SOBRIETY_START
    days = delta.days
    years = days // 365
    remainder = days % 365
    months = remainder // 30
    leftover = remainder % 30
    parts = []
    if years:
        parts.append(f"{years} year{'s' if years != 1 else ''}")
    if months:
        parts.append(f"{months} month{'s' if months != 1 else ''}")
    if leftover or not parts:
        parts.append(f"{leftover} day{'s' if leftover != 1 else ''}")
    streak = ", ".join(parts)
    return f"Sobriety streak: {days} days — {streak} since November 27, 2023. That is real."


def get_health_reminder():
    return (
        "Health check: Drink your gallon of water today. "
        "Keep it to one Monster or fewer. You know the deal."
    )


def get_github_activity():
    try:
        result = subprocess.run(
            ["gh", "api", "/users/thebardchat/events"],
            capture_output=True, text=True, timeout=15
        )
        events = json.loads(result.stdout)
        cutoff = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        # Go back 24 hours instead of midnight only
        from datetime import timedelta
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

        summaries = []
        seen = set()
        for event in events:
            created = event.get("created_at", "")
            try:
                event_time = datetime.fromisoformat(created.replace("Z", "+00:00"))
            except Exception:
                continue
            if event_time < cutoff:
                continue

            etype = event.get("type", "")
            repo = event.get("repo", {}).get("name", "unknown")
            payload = event.get("payload", {})

            if etype == "PushEvent":
                commits = payload.get("commits", [])
                for c in commits:
                    msg = c.get("message", "").split("\n")[0]
                    key = f"push:{repo}:{msg}"
                    if key not in seen:
                        seen.add(key)
                        summaries.append(f"Pushed to {repo}: {msg}")
            elif etype == "CreateEvent":
                ref = payload.get("ref", "")
                ref_type = payload.get("ref_type", "")
                key = f"create:{repo}:{ref}"
                if key not in seen:
                    seen.add(key)
                    summaries.append(f"Created {ref_type} {ref} in {repo}")
            elif etype == "IssuesEvent":
                action = payload.get("action", "")
                title = payload.get("issue", {}).get("title", "")
                key = f"issue:{repo}:{title}"
                if key not in seen:
                    seen.add(key)
                    summaries.append(f"{action.capitalize()} issue in {repo}: {title}")

        if summaries:
            lines = "\n  - ".join(summaries[:5])
            return f"GitHub last 24 hours:\n  - {lines}"
        return "GitHub: No commits or activity in the last 24 hours."
    except Exception as e:
        return f"GitHub: Could not fetch activity ({e})"


def get_motivational_line():
    return random.choice(MOTIVATIONAL_LINES)


def build_briefing():
    today = date.today()
    day_name = today.strftime("%A")
    date_str = today.strftime("%B %-d, %Y")

    sections = [
        f"Good morning Shane. Today is {day_name}, {date_str}.",
        "",
        get_weather(),
        "",
        get_sobriety(),
        "",
        get_health_reminder(),
        "",
        get_github_activity(),
        "",
        get_motivational_line(),
        "",
        "That is your briefing. Go get it. - ShaneBrain",
    ]
    return "\n".join(sections)


def send_ntfy(text):
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "-d", text, NTFY_URL],
            capture_output=True, text=True, timeout=15
        )
        code = result.stdout.strip()
        if code in ("200", "201", "204"):
            print(f"Delivered to {NTFY_URL} (HTTP {code})")
            return True
        print(f"ntfy returned HTTP {code}")
    except Exception as e:
        print(f"ntfy send failed: {e}")
    return False


def log_briefing(text):
    today = date.today().strftime("%Y-%m-%d")
    log_path = os.path.join(BRIEFING_LOG_DIR, f"{today}.txt")
    os.makedirs(BRIEFING_LOG_DIR, exist_ok=True)
    with open(log_path, "w") as f:
        f.write(text + "\n")
    print(f"Logged to {log_path}")


def main():
    print("Generating ShaneBrain daily briefing...")
    briefing = build_briefing()

    print("\n--- BRIEFING PREVIEW ---")
    print(briefing)
    print("--- END PREVIEW ---\n")

    log_briefing(briefing)
    delivered = send_ntfy(briefing)
    if not delivered:
        print("WARNING: ntfy delivery failed on all endpoints. Briefing saved to log only.")
        sys.exit(1)

    print("Done.")


if __name__ == "__main__":
    main()
