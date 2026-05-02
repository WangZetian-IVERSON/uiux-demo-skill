# AGENTS.md — UI/UX Portfolio Deck Skill

## What this is

A complete UI/UX portfolio deck builder skill. Read `SKILL.md` for the full
10-step pipeline and hard rules. This file is the entry point for agents that
don't auto-discover SKILL.md (Claude Code, Codex, custom agents).

## How to use this skill

1. **Read `SKILL.md` first** — it contains the Auto-Run sequence (10 steps),
   Hard Rules (MUST/Never), and the complete operating manual.

2. **The skill is invoked by any request about portfolio decks**, e.g.:
   - "做一份财务 SaaS 作品集"
   - "Create a UIUX case study for my running app"
   - "帮我 review 这个设计作品集的结构"

3. **On invocation, immediately run the Auto-Run sequence** starting from
   step 0 (Opening Checklist). Do NOT wait for the user to recite rules.

4. **Key reference files** (read when prompted by SKILL.md steps):
   - `references/image-prompt-style-uiux.md` — Default prompt format for UIUX pages
   - `references/image-generation-protocol.md` — Model routing + preset-first for posters
   - `references/headless-mode.md` — What to do when you can't run terminal commands
   - `references/page-patterns.md` — 7 layout patterns, variety enforcement
   - `references/closed-loop-overlay-qa.md` — Automated QA pipeline contract

5. **Scripts** — If you have terminal access, use the Python scripts in `scripts/`.
   All scripts read configuration from `scripts/config.py` (environment variables).
   If you do NOT have terminal access, follow `references/headless-mode.md`.

## Quick capability check

Before starting any work, silently determine:
- Can I execute `python scripts/...`? → FULL mode
- Can I generate images but not run scripts? → HEADLESS_GEN mode
- Neither? → HEADLESS_PROMPT_ONLY mode

State the mode at the end of step 1.

## Platform notes

- **GitHub Copilot**: Reads SKILL.md automatically. This AGENTS.md is redundant.
- **Claude Code**: Reads AGENTS.md and SKILL.md from the project root.
- **Codex (OpenAI)**: Reads AGENTS.md; may need SKILL.md content inlined if tool doesn't discover it.
- **Generic agent**: Place this folder in the project root. The agent should find AGENTS.md.
