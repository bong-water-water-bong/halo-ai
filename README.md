<div align="center">

# halo-ai

### The bare-metal AI stack for AMD Strix Halo

**Zero containers. Zero overhead. Every byte goes to inference.**

[![Arch Linux](https://img.shields.io/badge/Arch_Linux-1793D1?style=flat&logo=archlinux&logoColor=white)](https://archlinux.org)
[![ROCm](https://img.shields.io/badge/ROCm_7.13-ED1C24?style=flat&logo=amd&logoColor=white)](https://rocm.docs.amd.com)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

</div>

---

## What is this?

A complete, self-hosted AI platform compiled entirely from source for the **AMD Ryzen AI MAX+ 395 (Strix Halo)** APU. LLM inference, chat UI, deep research, voice I/O, image generation, RAG, and workflow automation — all running bare metal on a single chip with 128GB of unified memory.

## Design Philosophy

halo-ai is designed to run as a **dedicated, always-on AI server** built on a **minimal Arch Linux installation** — no desktop environment, no unnecessary packages, no bloat. The base system is a fresh `archinstall` with only the essentials: kernel, networking, SSH, Btrfs on LVM, and the packages required to compile the stack from source.

This is not a workstation setup where AI runs alongside a desktop. This is a headless server whose sole purpose is AI inference and serving. Every system resource — CPU cycles, memory, GPU compute, disk I/O — is dedicated to running models and serving requests. The minimal Arch base means:

- **No desktop environment** consuming GPU memory or CPU cycles
- **No package manager overhead** — every component is compiled from source with hardware-specific optimizations (`-DAMDGPU_TARGETS=gfx1151`, `-DGGML_HIP_ROCWMMA_FATTN=ON`)
- **No container runtime** stealing memory from the unified pool — on Strix Halo, CPU and GPU share the same 128GB, so every byte matters
- **Kernel-tuned GPU memory** — `amdgpu.gttsize=117760` reserves 115GB of the unified pool for GPU compute, leaving only what the OS needs
- **Always-on configuration** — sleep, suspend, hibernate, and lid switch are all disabled; power button is ignored
- **Automatic recovery** — a watchdog agent monitors all services every 5 minutes, auto-restarts failures, and only alerts when self-repair fails

The result: a quiet, headless box that boots into a fully operational AI platform and stays running 24/7, accessible over the network via web UIs and OpenAI-compatible APIs.

## What Makes This Different

There are excellent projects in the Strix Halo AI space — [DreamServer](https://github.com/Light-Heart-Labs/DreamServer) for a full orchestrated stack, [Lemonade](https://github.com/lemonade-sdk/lemonade) for AMD-optimized inference, [amd-strix-halo-toolboxes](https://github.com/kyuz0/amd-strix-halo-toolboxes) for containerized benchmarking, and [Framework community guides](https://github.com/Gygeek/Framework-strix-halo-llm-setup) for getting started. We recommend all of them.

halo-ai occupies a specific niche that none of them currently fill: **a complete AI stack compiled entirely from source, running bare metal, on a minimal headless server, optimized end-to-end for the Strix Halo unified memory architecture.**

- **Source-compiled for gfx1151** — Every GPU-accelerated binary is built with `-DAMDGPU_TARGETS=gfx1151` and ROCm Flash Attention (`rocWMMA`). No pre-built binaries, no AppImages, no generic builds. The compiler sees your exact hardware.
- **Unified memory as a first-class concern** — Strix Halo shares 128GB between CPU and GPU. halo-ai is architected around this: kernel-tuned GTT allocation (115GB for GPU), no container runtimes competing for the same memory pool, systemd isolation instead of Docker. Every architectural decision maximizes memory available for model inference.
- **Full stack, not just inference** — This is not a llama.cpp wrapper. It is 10 integrated services — LLM inference, chat UI, deep research, voice I/O, image generation, RAG, search, and workflow automation — all running on one chip with zero external dependencies.
- **Server-first** — Built for 24/7 headless operation on a minimal Arch install, with a watchdog agent, automatic Btrfs snapshots, and systemd service management. Not a desktop application.

## Hardware Target

This stack is built exclusively for the Strix Halo unified memory architecture:

| Component | Spec |
|-----------|------|
| **APU** | AMD Ryzen AI MAX+ 395 (Strix Halo) |
| **CPU** | 16 Zen 5 cores / 32 threads, 5.19 GHz, AVX-512 |
| **GPU** | Radeon 8060S — RDNA 3.5, 40 CUs, gfx1151 |
| **NPU** | AMD XDNA 2 — 50 TOPS |
| **Memory** | 128GB LPDDR5x-8000 unified (~215 GB/s) |
| **GPU Compute** | 115 GB via GTT (kernel-tuned) |

The killer feature of Strix Halo is unified memory — CPU and GPU share the full 128GB pool. With kernel-level GTT tuning, 115GB is accessible for GPU compute. No consumer discrete GPU comes close. This means models that would require a $10,000+ multi-GPU setup elsewhere run on a single chip here.

## What you can run

| Model | Quantization | Size | Speed |
|-------|-------------|------|-------|
| Llama 3 8B | Q4_K_M | ~5 GB | ~45 tok/s |
| Qwen 3 30B-A3B (MoE) | Q4_K_M | ~18 GB | ~72 tok/s |
| Llama 3 70B | Q4_K_M | ~40 GB | ~15-20 tok/s |
| Llama 3 70B | Q8_0 | ~70 GB | ~8-12 tok/s |
| DeepSeek V3 (MoE) | Q4_K_M | ~95 GB | ~5-10 tok/s |
| GPT-OSS 120B (MoE) | Q4 | ~63 GB | ~40-47 tok/s |

## Services

| Service | Port | Purpose |
|---------|------|---------|
| **Lemonade** | 8080 | Unified AI API (OpenAI + Ollama + Anthropic compatible) |
| **llama.cpp** | 8081 | LLM inference (HIP + Vulkan dual backends) |
| **Open WebUI** | 3000 | Chat interface with RAG, document upload, multi-model |
| **Vane** | 3001 | Deep research engine (Perplexica) |
| **SearXNG** | 8888 | Private meta-search engine |
| **Qdrant** | 6333 | Vector database for RAG embeddings |
| **n8n** | 5678 | Workflow automation (400+ integrations) |
| **whisper.cpp** | 8082 | Speech-to-text (ROCm accelerated) |
| **Kokoro** | 8083 | Text-to-speech |
| **ComfyUI** | 8188 | Image generation (PyTorch ROCm) |

## Architecture

```
User Interfaces                    AI Research
┌──────────────┐                  ┌──────────────┐
│  Open WebUI  │ :3000            │    Vane      │ :3001
│  n8n         │ :5678            │  (Perplexica)│
└──────┬───────┘                  └──────┬───────┘
       │ OpenAI-compatible API           │
       ▼                                 ▼
┌──────────────────────────────────────────────┐
│              Lemonade Server                  │ :8080
│  OpenAI + Ollama + Anthropic API compatible  │
└───────┬──────────────┬───────────────┬───────┘
        ▼              ▼               ▼
   llama.cpp      whisper.cpp       Kokoro
   HIP + Vulkan   (STT)            (TTS)
        │
   ┌────┴──────────────────────────────┐
   │  ROCm 7.13  →  gfx1151           │
   │  /dev/kfd + /dev/dri (direct)     │
   │  115 GB GTT  │  ~215 GB/s BW     │
   └───────────────────────────────────┘

Supporting Services:
  SearXNG :8888 ← Vane (web search)
  Qdrant  :6333 ← Open WebUI (RAG embeddings)
  n8n     :5678 → Lemonade (LLM in workflows)
```

## Isolation Without Containers

Every service runs as a systemd unit with process isolation, auto-restart, and resource limits — zero memory overhead. Dependencies are isolated with Python venvs and separate Node.js installs. Data is isolated with Btrfs subvolumes, each with independent snapshot capability.

| Layer | What It Provides | Overhead |
|-------|-----------------|----------|
| **systemd units** | Process isolation, auto-restart, `MemoryMax`/`CPUQuota`, journald logging | 0 bytes |
| **Python venvs** | Per-service dependency isolation — immune to system updates | ~50 MB each |
| **Btrfs subvolumes** | Per-service data isolation, instant snapshots, atomic rollback | 0 bytes (metadata) |
| **Snapper** | Automatic hourly/daily/weekly snapshots + pre/post on pacman ops | 0 bytes (COW) |
| **udev rules** | Persistent GPU device permissions (`/dev/kfd`, `/dev/dri`) | 0 bytes |

Clean uninstall of any service: `btrfs subvolume delete /srv/ai/<service>`

## Directory Layout

```
/srv/ai/
├── configs/          ← Shared configuration (ROCm env, SearXNG, Qdrant)
├── systemd/          ← All service unit files
├── scripts/          ← Build and maintenance scripts
├── models/           ← Shared model storage (GGUF, safetensors)
│
├── rocm/             ← ROCm 7.13 SDK (TheRock nightly, gfx1151)
├── llama-cpp/        ← llama.cpp (build-hip/ + build-vulkan/)
├── lemonade/         ← Lemonade 10.0.1 (lemonade-server + lemonade-router)
├── whisper-cpp/      ← whisper.cpp (ROCm accelerated)
│
├── open-webui/       ← Open WebUI 0.8.10 (Python 3.12 venv)
├── vane/             ← Vane/Perplexica (Node.js 24.5)
├── searxng/          ← SearXNG (Python 3.14 venv)
├── qdrant/           ← Qdrant 1.17.0 (Rust static binary)
├── n8n/              ← n8n 2.14.0 (Node.js 24.5)
├── kokoro/           ← Kokoro TTS (Python 3.13 venv + PyTorch ROCm)
└── comfyui/          ← ComfyUI (Python 3.13 venv + PyTorch ROCm 6.2.4)
```

## Build Stack

Everything compiled from source on the target hardware:

| Component | Version | Compiler/Toolchain |
|-----------|---------|-------------------|
| ROCm | 7.13 (TheRock nightly) | AMD Clang 23.0 |
| llama.cpp | latest | HIP + Vulkan, gfx1151, rocWMMA FA |
| Lemonade | 10.0.1 | CMake + Ninja |
| whisper.cpp | latest | HIP, gfx1151 |
| Qdrant | 1.17.0 | Rust 1.94, cargo release |
| Node.js | 24.5.0 | GCC 15.2 |
| Python | 3.12.13 / 3.13.3 / 3.14.3 | GCC 15.2, `--enable-optimizations` |
| Open WebUI | 0.8.10 | pip (Python 3.12 venv) |
| Vane | latest | Yarn 4.13 (Node.js 24.5) |
| n8n | 2.14.0 | pnpm (Node.js 24.5) |
| ComfyUI | latest | PyTorch 2.7.1+rocm6.2.4 |

## Watchdog Agent

A watchdog agent runs every 5 minutes via systemd timer. It:

- Monitors all service health and auto-restarts failed services
- Checks GPU device availability and temperature
- Monitors disk usage and available memory
- Checks all upstream repos for available updates
- Checks for kernel and system package updates
- **Only alerts when auto-repair fails** — silent when everything is healthy

```bash
journalctl -t halo-watchdog        # Watchdog entries
cat /var/log/halo-watchdog.log     # Full log
```

## Snapshot Policy

Snapper manages automatic Btrfs snapshots on `/` and `/home`:

| Retention | Count |
|-----------|-------|
| Hourly | 24 |
| Daily | 14 |
| Weekly | 4 |
| Monthly | 6 |
| Yearly | 10 |
| Pacman pre/post | Automatic (snap-pac) |

## Credits & Acknowledgements

- **[DreamServer](https://github.com/Light-Heart-Labs/DreamServer)** by Light-Heart-Labs — The original vision of a complete, integrated AI stack for Strix Halo. DreamServer proved that Strix Halo could run a full AI platform — not just a single model — and showed what was possible. halo-ai takes that vision and rebuilds it bare-metal for maximum performance on unified memory hardware.

- **[Lemonade](https://github.com/lemonade-sdk/lemonade)** by AMD / Lemonade SDK — The unified AI serving layer that makes this entire stack practical. Their dedicated work on gfx1151 ROCm support, NPU+GPU hybrid inference, and the llamacpp-rocm nightly builds has been essential for making Strix Halo a viable AI platform.

- **[llama.cpp](https://github.com/ggml-org/llama.cpp)**, **[Open WebUI](https://github.com/open-webui/open-webui)**, **[Vane](https://github.com/ItzCrazyKns/Vane)**, **[whisper.cpp](https://github.com/ggerganov/whisper.cpp)**, **[Kokoro](https://github.com/remsky/Kokoro-FastAPI)**, **[ComfyUI](https://github.com/comfyanonymous/ComfyUI)**, **[SearXNG](https://github.com/searxng/searxng)**, **[Qdrant](https://github.com/qdrant/qdrant)**, **[n8n](https://github.com/n8n-io/n8n)**, **[ROCm/TheRock](https://github.com/ROCm/TheRock)** — The open-source projects that make this stack possible.

## License

Apache 2.0
