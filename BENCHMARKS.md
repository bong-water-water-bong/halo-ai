# halo-ai Benchmark Results

**Date**: 2026-03-24
**Hardware**: AMD Ryzen AI MAX+ 395 (Strix Halo), 128GB LPDDR5x-8000
**Kernel**: 6.19.9-arch1-1
**ROCm**: 7.13 (TheRock nightly, gfx1151)
**GPU Memory (GTT)**: 115 GB (123,480,309,760 bytes)
**Backend**: llama.cpp HIP + rocWMMA Flash Attention

## Inference Performance

**Model**: Qwen3-30B-A3B (MoE, Q4_K_M, 18GB)

| Test | Prompt Tokens | Generated Tokens | Prompt Speed | Generation Speed | Total Time |
|------|--------------|-----------------|-------------|-----------------|------------|
| Short prompt (14 tok) | 14 | 200 | 236.0 tok/s | 71.6 tok/s | 2.85s |
| Long prompt (30 tok) | 30 | 500 | 323.3 tok/s | 69.2 tok/s | 7.32s |

### Key Metrics

- **Generation throughput**: ~70 tok/s sustained
- **Prompt processing**: 236-323 tok/s depending on length
- **Time to first token**: <100ms
- **Model load time**: ~5s (18GB to GPU via unified memory)

### Context

MoE (Mixture of Experts) models are the sweet spot for Strix Halo's unified memory architecture. The 30B-A3B variant activates ~3B parameters per token while having 30B total, giving high quality output with fast generation. Dense 70B models achieve ~15-20 tok/s on the same hardware.

## Service Memory Usage

All services running simultaneously:

| Service | Memory | Notes |
|---------|--------|-------|
| llama-server (Qwen3-30B) | 657 MB | + ~18GB GPU VRAM for model |
| Open WebUI | 3,238 MB | Includes ML models for embeddings |
| Qdrant | 514 MB | Vector DB (empty, will grow with data) |
| ComfyUI | 509 MB | PyTorch ROCm loaded |
| n8n | 438 MB | Workflow engine |
| SearXNG | 94 MB | Lightweight search proxy |
| Vane (Perplexica) | 35 MB | Next.js server |
| Lemonade | 20 MB | C++ router, very lightweight |
| **Total service overhead** | **~5.5 GB** | |

**System total**: 27 GB used out of 128 GB — leaving ~97 GB available for model loading, with 115 GB GPU-addressable via GTT.

## GPU Thermals Under Load

| State | GPU Temperature | GPU Utilization |
|-------|----------------|-----------------|
| Idle | 26°C | 0% |
| Inference (Qwen3-30B) | 49°C | 92% |

Well within thermal limits (critical: 100°C). No throttling observed.

## System Boot

| Phase | Time |
|-------|------|
| Firmware | 6.9s |
| Bootloader | 3.5s |
| Kernel | 5.4s |
| Userspace | 3.4s |
| **Total** | **19.3s** |

No failed units. No errors. Two known amdgpu warnings on headless boot (HDMI CRTC timeout — cosmetic, no impact).
