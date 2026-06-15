# venture-compass

An **autonomous co-pilot for solo, AI-built micro-ventures** — small apps, sites, and bots aimed at
quickly filling a low-competition vacuum and getting traction (users, revenue, or just popularity).

You build the project; **the agent drives the lifecycle.** It briefs you at session start, watches
the kill dates / live metrics / external landscape, and itself decides when to run a decision gate.
At each gate it convenes a thorough **adversarial consilium** of subagent "lenses" that judge **blind
and independently**, then a synthesizer fuses them into one honest verdict — **GO / PIVOT / KILL /
SCALE**. State persists across sessions in `VENTURE.md`. **Default bias: kill on time.**

> The runtime output (briefings, the panel, verdicts, and everything written to `VENTURE.md` /
> `LANDSCAPE.md`) is in **Russian**. The plugin's internal instructions are in English.

## Install

```bash
claude --plugin-dir /path/to/parent-of-venture-compass
# then, inside Claude Code:
/reload-plugins
```

`--plugin-dir` points at the directory **containing** `venture-compass/`. Once loaded, the
`managing-microventures` skill, the nine agents, the four commands, and the state hook are all active.

## Use

**Just talk about your project.** The agent takes it from there:

- Mention a new idea, ask "стоит ли браться?", or "how's X going?" — it briefs and runs the right
  gate.
- It runs checkpoints itself when a kill date hits, a metric breaches a threshold, or it sees drift.
- **One-time setup:** add these to your project's `CLAUDE.md` so state auto-loads every session and
  survives `/compact`:

  ```markdown
  @VENTURE.md
  @LANDSCAPE.md
  ```

The four slash commands are **manual overrides only** — briefing, landscape scans, and metric pulls
all happen automatically:

| Command | Effect |
|---------|--------|
| `/audit [area]` | Force a Gate 2 checkpoint now (live metrics → blind consilium → verdict). |
| `/kill [reason]` | Close the venture manually (confirm once; irreversible). |
| `/override [change]` | Reject or hold the agent's last call (logged; never erases a fired trigger). |
| `/details` | Read-only expansion of the last consilium. |

## The four gates (Stage-Gate spine)

| Gate | Fires when | Lenses convened | Verdict |
|------|-----------|-----------------|---------|
| **0 · Браться ли** | a raw idea, before setup | 🕳 demand-scout, 👾 tech-skeptic, ⚔️ devils-advocate, 🃏 lateral | GO-INTO-SETUP / DROP |
| **1 · Сетап линий** | fixing success & kill criteria | ⚔️ devils-advocate (pre-mortem), ⏳ keeper-of-time, 💼 business-pragmatist, 🃏 lateral | the written lines + the named monkey |
| **2 · Чекпоинт** | a date hits / metric breaches / drift / on request | ⏳, 👾, 💼, 🕳, ⚔️ as the **Жизнь vs Смерть** pair, 🃏 | GO / PIVOT / KILL / SCALE |
| **3 · Пивот** | Gate 2 returned PIVOT | 4 ephemeral generators (audience / problem / solution / channel) + 🃏 | one single-element pivot, or KILL |

KILL and SCALE are verdicts of Gate 2, not separate gates. The 🃏 lateral seat sits on every gate.

## Grounded in proven practice

Stage-Gate (Cooper) · Lean Startup (Ries) · Lean Canvas (Maurya) · The Mom Test (Fitzpatrick) ·
kill criteria (Annie Duke) · Discovery-Driven Planning (McGrath & MacMillan) · AARRR (McClure) + One
Metric That Matters (Croll & Yoskovitz) · Bullseye (Weinberg) · pre-mortem (Klein). The consilium
engine: Dialectical Inquiry / Devil's Advocacy (Schweiger, Sandberg & Ragan, *AMJ* 1986), the
Mediating Assessments Protocol (Kahneman, *Noise*), and the anti-groupthink rule — judge
independently first, synthesize second (Asch / Janis).

## Notes

- Runs in **Claude Code** (skills, subagents, hooks, slash commands).
- The state hook (`hooks/scripts/check-state.py`) runs at session start and stop. At session start it
  mixes prior `VENTURE.md` state + **live metrics** + landscape staleness into context. It is
  defensive — never blocks a session, always exits 0, reads state files with a size cap, and stays
  completely silent if there's no `VENTURE.md`.
- **Security — the metrics collector is project-local code.** The hook runs `scripts/metrics/collect.*`
  **only when `VENTURE.md` marks the source `✔ verified`**, so merely opening some other repo that
  happens to contain a collector does **not** execute it. It runs in its own process group with a
  timeout and `cwd` at the project root, and treats the collector's output as untrusted (one line,
  length-capped, control characters stripped; raw stderr is never echoed into context). Marking a
  source `✔ verified` = authorizing that script to run on session start.
- **Secrets** (API tokens for the collector) are read from **environment variables**, never written
  into files.
