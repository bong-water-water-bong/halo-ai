# strix-halo AI Stack

Bare-metal AI inference stack compiled from source for AMD Ryzen AI MAX+ 395 (Strix Halo).

## Hardware
- CPU: AMD Ryzen AI MAX+ 395 (16C/32T, Zen 5, AVX-512)
- GPU: Radeon 8060S (RDNA 3.5, 40 CUs, gfx1151)
- NPU: AMD XDNA 2 (50 TOPS)
- RAM: 128GB LPDDR5x-8000 unified memory
- Storage: 1.9TB YMTC NVMe (Btrfs on LVM)
- OS: Arch Linux, kernel 6.19.9

## Services

| Service | Port | Purpose |
|---------|------|---------|
| Lemonade | 8080 | Unified LLM API (OpenAI-compatible) |
| llama.cpp | (backend) | LLM inference (HIP + Vulkan) |
| Open WebUI | 3000 | Chat interface |
| Vane (Perplexica) | 3001 | Deep research engine |
| SearXNG | 8888 | Private web search |
| Qdrant | 6333 | Vector DB for RAG |
| n8n | 5678 | Workflow automation |
| whisper.cpp | (backend) | Speech-to-text |
| Kokoro | (backend) | Text-to-speech |
| ComfyUI | 8188 | Image generation |

## Architecture
- All services compiled from source
- Each service in its own Btrfs subvolume under /srv/ai/
- Python services isolated with venvs
- systemd units for process management
- ROCm via TheRock nightly (gfx1151)
- Snapper for automatic Btrfs snapshots

## GPU Memory
Kernel param `amdgpu.gttsize=117760` allocates ~115GB for GPU compute.
