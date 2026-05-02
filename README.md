# UI/UX quickPortfolio-demo  — AI Skill

A portable skill for building UI/UX portfolio decks and product design case-study presentations. One prompt → complete image-rich deck with automated quality review.

Works with **GitHub Copilot**, **Claude Code**, **Codex (OpenAI)**, and any AI coding agent that supports skill files.

## Quick Start

### 1. Install the skill

**VS Code / GitHub Copilot** (easiest):
```
Copy this entire folder into your project.
The SKILL.md is auto-discovered by Copilot.
```

**Claude Code**:
```bash
# Clone into your CLAUDE.md project
git clone https://github.com/<your-username>/uiux-portfolio-deck.git
# Claude reads SKILL.md as a project instruction file
```

**Codex / OpenAI**:
```bash
git clone https://github.com/<your-username>/uiux-portfolio-deck.git
cd uiux-portfolio-deck
# The AGENTS.md + SKILL.md files provide instructions to the agent
```

### 2. Install Python dependencies

```bash
pip install pillow playwright
playwright install chromium
```

### 3. Set up your image generation backend

The skill auto-detects available tools. Set environment variables for the backend you use:

```powershell
# Option A: pockgo relay (default)
$env:BACKEND_API_KEY = "sk-your-key"
$env:BACKEND_BASE_URL = "https://api.openai.com/v1"

# Option B: Direct OpenAI
$env:BACKEND_API_KEY = "sk-your-openai-key"
$env:BACKEND_BASE_URL = "https://api.openai.com/v1"

# Option C: ComfyUI Desktop (local)
$env:COMFY_API_KEY = "your-comfy-key"
# No BACKEND_* needed — image_client.py --backend comfyui
```

All configuration lives in `scripts/config.py`. See that file for every supported variable.

### 4. Start building

Type one sentence in the AI chat:

> "做一份财务 SaaS 作品集"

The skill auto-runs a 10-step pipeline: gathers requirements → picks style → generates images → builds HTML overlays → runs quality review.

## What This Skill Does

```
User says "做一个XX作品集"
        │
        ▼
┌──────────────────────────────────────────┐
│ Auto-Run 10-Step Pipeline                 │
│                                           │
│ 0. OPENING CHECKLIST (missing info?)      │
│ 1. CAPABILITY CHECK (what tools exist?)   │
│ 2. ASSET SCAN (screenshots? brand?)       │
│ 3. SCOPE DECIDE (case study vs proposal)  │
│ 4. STYLE PICK (visual direction)          │
│ 5. LOCK ART DIRECTION (PADB)              │
│ 6. ASSET ROUTING (image vs HTML per page) │
│ 7. SHOWCASE FIRST (cover → QA → confirm)  │
│ 8. CONFIRM (user approves visual grammar) │
│ 9. EXPAND (batch-produce all pages)       │
│ 10. CLOSED-LOOP QA (auto-fix overlays)    │
└──────────────────────────────────────────┘
        │
        ▼
   Complete HTML deck
   (image backgrounds + text overlays + navigation)
```

## Operating Modes

The skill auto-detects your environment:

| Mode | Terminal? | Image tool? | What you get |
|------|-----------|-------------|--------------|
| **FULL** | ✅ | ✅ | Automated pipeline: image gen → overlay build → auto QA fix loop |
| **HEADLESS_GEN** | ❌ | ✅ | Agent writes prompts; you run image model externally; agent does manual visual QA |
| **HEADLESS_PROMPT_ONLY** | ❌ | ❌ | Prompt pack (`.txt` files + `layout.json` files + README) — you run everything externally |

## File Structure

```
uiux-portfolio-deck/
├── SKILL.md                          # Main skill definition (the agent's brain)
├── AGENTS.md                         # Compatibility layer for non-Copilot agents
├── README.md                         # This file
├── .gitignore
├── references/                       # 30+ reference docs (rules, protocols, checklists)
│   ├── image-prompt-style-uiux.md    #   → Default UIUX prompt paradigm
│   ├── image-generation-protocol.md  #   → Model routing & prompt structure
│   ├── headless-mode.md              #   → Degradation path + Manual QA Checklist
│   ├── page-patterns.md              #   → 7 page patterns + layout variety rules
│   ├── closed-loop-overlay-qa.md     #   → Automated QA pipeline
│   └── ...                           #   → 25+ more
├── scripts/                          # Python toolchain (config-driven, no hardcoded URLs)
│   ├── config.py                     #   → Unified backend configuration
│   ├── image_client.py               #   → Image generation (pockgo/OpenAI/ComfyUI)
│   ├── build_with_qa.py              #   → Closed-loop overlay QA
│   ├── build_interactive_page.py     #   → HTML overlay builder
│   ├── render_screenshot.py          #   → Playwright screenshot
│   └── ...
└── vendor/                           # Deck stage & export tools
    └── design-assets/
        ├── assets/deck_stage.js      #   → Keyboard navigation + page switching
        └── scripts/                  #   → PDF/PPTX export
```

## Requirements

- **Python 3.10+** with `pillow`, `playwright`
- **Playwright Chromium** (`playwright install chromium`)
- **An image generation backend** (pick one):
  - pockgo relay (OpenAI-compatible, default)
  - OpenAI API (direct)
  - ComfyUI Desktop (local)
- **A vision-capable LLM** for QA (uses same backend as configured)

## Configuration Reference

See `scripts/config.py` for all options. Quick reference:

| Variable | Default | What |
|----------|---------|------|
| `BACKEND_API_KEY` | (falls back to `OPENAI_KEY`) | API key |
| `BACKEND_BASE_URL` | `https://api.openai.com/v1` | Relay/provider URL |
| `BACKEND_IMAGE_MODEL` | `gpt-image-2` | Default image model |
| `BACKEND_QA_MODEL` | `gpt-4o` | Vision QA model |
| `COMFY_API_KEY` | — | ComfyUI key (separate) |
| `COMFYUI_URL` | `http://127.0.0.1:XXXX` | ComfyUI server |

## License

MIT — see `vendor/design-assets/LICENSE`.
