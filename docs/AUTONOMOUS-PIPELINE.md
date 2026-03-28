# halo-ai studios — Autonomous Pipeline Architecture

## Overview

A fully autonomous game studio running on a single Strix Halo machine.
17 agents handle everything from code to customer. Zero human interaction
with the outside world. The user builds agents. Agents run the business.

## The Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT PHASE                             │
│                                                                  │
│  Developer pushes code                                           │
│       ↓                                                          │
│  sentinel (code watcher)                                         │
│       ├── Reviews PR (static analysis + LLM)                    │
│       ├── Security scan → meek                                   │
│       ├── Bug check → bounty                                     │
│       ├── Clean? → auto-merge                                    │
│       └── Blocked? → request changes                             │
│       ↓                                                          │
│  meek (security chief)                                           │
│       ├── Vulnerability scan                                     │
│       ├── Dependency audit                                       │
│       ├── Anti-cheat integrity check                             │
│       └── ghost (secrets) → validates no leaked credentials      │
│       ↓                                                          │
│  bounty (QA / bug hunter)                                        │
│       ├── Automated test suite                                   │
│       ├── Regression testing                                     │
│       ├── Performance benchmarks                                 │
│       └── Bug report triage                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BUILD PHASE                                 │
│                                                                  │
│  forge (game builder)                                            │
│       ├── Export: Linux (x86_64)                                 │
│       ├── Export: Windows (x86_64)                               │
│       ├── Export: macOS (universal)                               │
│       ├── Asset pipeline: interpreter → ComfyUI → Blockbench     │
│       ├── Audio pipeline: amp → SFX/music/voice                  │
│       └── Build validation (file sizes, required files, no debug)│
│       ↓                                                          │
│  interpreter (creative director)                                 │
│       ├── Enhances all generation prompts                        │
│       ├── Maintains visual style consistency                     │
│       └── Art direction for new content                          │
│       ↓                                                          │
│  amp (audio engineer)                                            │
│       ├── SFX generation and mastering                           │
│       ├── Music production                                       │
│       ├── Trailer audio                                          │
│       └── Voice line processing                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT PHASE                               │
│                                                                  │
│  forge:steam (Steam deployer)                                    │
│       ├── Generate VDF manifests                                 │
│       ├── Pre-upload security check (meek approval required)     │
│       ├── SteamCMD upload (Linux/Windows/Mac depots)             │
│       ├── Build manifest tracking                                │
│       └── Rollback capability (vault snapshots)                  │
│       ↓                                                          │
│  vault (backup / disaster recovery)                              │
│       ├── Pre-deploy snapshot                                    │
│       ├── Post-deploy snapshot                                   │
│       ├── Rollback on failure                                    │
│       └── Build artifact archival                                │
│       ↓                                                          │
│  pulse (DevOps / monitoring)                                     │
│       ├── Monitor deployment health                              │
│       ├── Track download counts, crash reports                   │
│       ├── Performance metrics                                    │
│       └── Alert on anomalies → echo                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   COMMUNITY PHASE                                │
│                                                                  │
│  echo (public face)                                              │
│       ├── Discord: patch notes, announcements, player chat       │
│       ├── Steam: store page updates, community posts             │
│       ├── Social media: release announcements                    │
│       ├── Bug reports: receives from players → bounty            │
│       ├── Feature requests: log and prioritize                   │
│       └── Personality: friendly, professional, slightly witty    │
│       ↓                                                          │
│  shield (player protection)                                      │
│       ├── Content moderation (Discord, Steam forums)             │
│       ├── Toxicity filtering                                     │
│       ├── Player report handling                                 │
│       └── Community guidelines enforcement                       │
│       ↓                                                          │
│  fang (intrusion detection)                                      │
│       ├── Detect cheating in real-time                            │
│       ├── Ban enforcement                                        │
│       ├── Exploit detection and reporting → bounty               │
│       └── Anti-tamper monitoring                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  IN-GAME (RUNTIME)                                │
│                                                                  │
│  dealer (game master AI)                                         │
│       ├── Local LLM (3B-7B, GGUF, runs on player's machine)     │
│       ├── Enemy AI tactics (real-time decisions)                 │
│       ├── World generation (intelligent dungeon design)          │
│       ├── Dynamic events (emergent, never scripted)              │
│       ├── Intelligent loot placement                             │
│       ├── Difficulty adaptation (invisible to player)            │
│       ├── Room narration (atmospheric, unique each run)          │
│       └── Player profiling (adapts to play style)                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                 INFRASTRUCTURE (ALWAYS ON)                        │
│                                                                  │
│  halo (CEO / orchestrator)                                       │
│       ├── Service management (start/stop/restart all agents)     │
│       ├── Health monitoring across all agents                    │
│       └── Escalation when agents can't resolve issues            │
│                                                                  │
│  pulse (health monitor)                                          │
│       ├── All services uptime tracking                           │
│       ├── Resource usage (CPU, RAM, GPU, disk)                   │
│       └── Alert cascade when thresholds exceeded                 │
│                                                                  │
│  net (network operations)                                        │
│       ├── Multiplayer server management (Phase 2)                │
│       ├── DDoS protection                                        │
│       ├── Latency monitoring                                     │
│       └── DDNS via ASUS router                                   │
│                                                                  │
│  gate (access control)                                           │
│       ├── Authentication for multiplayer                         │
│       ├── DLC license validation                                 │
│       ├── API rate limiting                                      │
│       └── Permission management                                  │
│                                                                  │
│  ghost (secrets management)                                      │
│       ├── API keys, tokens, credentials                          │
│       ├── Steam API keys                                         │
│       ├── Discord bot tokens                                     │
│       └── Rotation and audit                                     │
│                                                                  │
│  mirror (privacy / compliance)                                   │
│       ├── PII scanning (no player data leaked)                   │
│       ├── GDPR compliance                                        │
│       ├── Steam / store policy compliance                        │
│       └── Audit trail                                            │
│                                                                  │
│  vault (backup / DR)                                             │
│       ├── Automated snapshots (btrfs)                            │
│       ├── Build artifact storage                                 │
│       ├── Player save backup (Phase 2)                           │
│       └── Instant rollback capability                            │
└─────────────────────────────────────────────────────────────────┘

## Message Bus

All agents communicate via the halo-ai message bus (port 8100).

Topics:
- security    — meek, ghost, fang, mirror, sentinel
- bugs        — bounty, sentinel, echo
- releases    — forge, echo, vault, pulse
- community   — echo, shield
- builds      — forge, sentinel, meek
- monitoring  — pulse, net, halo
- game        — dealer, forge

Message format:
{
  "from": "sentinel",
  "topic": "builds",
  "event": "pr_merged",
  "payload": {"repo": "voxel-extraction", "pr": 42},
  "timestamp": "2026-03-28T04:30:00Z"
}

## Hardware

- Strix Halo (ops center): Ryzen AI MAX+ 395, 128GB unified
  - Runs: all agents, llama.cpp (for sentinel/echo/dealer LLM review),
    ComfyUI (asset gen), message bus, monitoring
  - Accessible at: http://strixhalo (Caddy on port 80)
  - SSH: 192.168.50.69

- ryzen (dev machine): 9800X3D, Navi 48
  - Runs: Godot editor, development, testing, glass dock

- sligar (backup): 8700K, 1080Ti
  - Runs: secondary workloads, backup compute

## Deployment: One Command

```bash
# On any Strix Halo machine:
curl -sSL https://raw.githubusercontent.com/bong-water-water-bong/halo-ai/main/install.sh | bash
```

This installs:
1. All agent repos
2. Python environments (standalone, isolated)
3. llama.cpp with a small model for agent LLM tasks
4. ComfyUI for asset generation
5. Message bus
6. systemd services for all agents
7. Caddy reverse proxy
8. The game itself (voxel-extraction)

## Revenue

- Base game: $19.95 (includes The Undercroft)
- DLC dungeon packs: $4.99-$9.99
- Community marketplace: creator-set pricing
- AMD developer challenges (Lemonade, Pervasive AI)

## Proving the Concept

Demo video for AMD challenges:
1. Show the Strix Halo machine
2. Run the installer
3. Show agents booting up
4. Push a code change → sentinel reviews → forge builds → echo announces
5. Launch the game → dealer runs AI → every run different
6. Show Man Cave dashboard with all agents visible
7. "One machine. 17 agents. Zero cloud. This is halo-ai."
