# ShaneBrain Daily Briefing

Good morning briefing system for Shane Brazelton — 6am push notification via ntfy, running on shanebrain-1 (Pi 5).

## What it delivers

Every morning at 6am you get a plain-text, voice-friendly briefing with:

- Weather for Hazel Green, Alabama
- Sobriety streak (since November 27, 2023)
- Health reminder — Monster taper + water goal
- GitHub activity from the last 24 hours
- A motivational line in Shane's real voice
- Sign-off from ShaneBrain

No markdown. No asterisks. Just clean text to read or have read to you.

## Setup

```bash
# Clone into shanebrain-core
cd /mnt/shanebrain-raid/shanebrain-core
git clone https://github.com/thebardchat/shanebrain-briefing

# Create log directory
mkdir -p /mnt/shanebrain-raid/shanebrain-core/briefings

# Install systemd timer
sudo cp systemd/shanebrain-briefing.service /etc/systemd/system/
sudo cp systemd/shanebrain-briefing.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now shanebrain-briefing.timer

# Test it manually
python3 /mnt/shanebrain-raid/shanebrain-core/shanebrain-briefing/briefing.py
```

## ntfy subscription

Subscribe on your phone: `ntfy.sh/shanebrain-briefing` or use self-hosted instance at `localhost:80/shanebrain-briefing`.

## Logs

Each briefing is saved to `/mnt/shanebrain-raid/shanebrain-core/briefings/YYYY-MM-DD.txt`.

---

Built by Shane Brazelton + Claude (Anthropic) — ShaneBrain ecosystem, shanebrain-1, Pi 5

> New to Claude? [Get started here](https://claude.ai/referral/4fAMYN9Ing)
