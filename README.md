<div align="center">

# ShaneBrain Daily Briefing

> **Try Claude free for 2 weeks** — the AI behind this entire ecosystem. [Start your free trial →](https://claude.ai/referral/4fAMYN9Ing)

---

**6am push notification + spoken briefing for Shane Brazelton — running on shanebrain-1 (Pi 5, Hazel Green AL).**

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![ntfy](https://img.shields.io/badge/Delivery-ntfy.sh-green)](https://ntfy.sh)
[![systemd](https://img.shields.io/badge/Scheduler-systemd%20timer-orange)]()
[![ShaneBrain](https://img.shields.io/badge/Part%20of-ShaneBrain-blueviolet)](https://github.com/thebardchat/shanebrain-core)

</div>

---

## What it delivers

Every morning at 6am:

| Section | Source |
|---------|--------|
| Date and greeting | System clock |
| Weather | wttr.in — Hazel Green, Alabama |
| Sobriety streak | Days since November 27, 2023 |
| Health reminder | Monster taper + water goal |
| GitHub activity | Last 24 hours via `gh api` |
| Motivational line | 10 rotating lines in Shane's real voice |
| Sign-off | ShaneBrain |

Plain text throughout — no markdown symbols, no asterisks. Reads clean on a phone notification or spoken aloud via TTS.

---

## Delivery

- **Push notification** — `ntfy.sh/shanebrain-briefing` (subscribe on your phone)
- **Spoken aloud** — espeak-ng → aplay via local audio hardware (when connected)
- **Log file** — `/mnt/shanebrain-raid/shanebrain-core/briefings/YYYY-MM-DD.txt`

---

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

# Test manually
python3 briefing.py
```

---

## Repo structure

```
briefing.py                  Main briefing script — builds and delivers
systemd/
├── shanebrain-briefing.service   Runs both ntfy push and TTS playback
└── shanebrain-briefing.timer     Fires at 6:00 AM daily (Persistent=true)
```

---

## TTS audio

Audio playback is handled by [pico-nerve-endings](https://github.com/thebardchat/pico-nerve-endings) — the `tts_briefing.py` host script imports `build_briefing()` from this repo and speaks it via espeak-ng.

```bash
# Play locally (USB speaker or HDMI audio)
python3 /path/to/pico-nerve-endings/projects/audio-speaker/host/tts_briefing.py --local

# Stream to Pico 2 audio speaker
python3 /path/to/pico-nerve-endings/projects/audio-speaker/host/tts_briefing.py
```

---

<div align="center">

*Built by Shane Brazelton + Claude (Anthropic) — ShaneBrain ecosystem, shanebrain-1, Pi 5.*

*Faith · Family · Sobriety · Local AI · The Left-Behind User*

</div>
