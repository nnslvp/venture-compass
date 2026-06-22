# CLAUDE.md — developing the venture-compass plugin

This repo **is** the `venture-compass` Claude Code plugin (and doubles as a single-plugin
**marketplace** via `.claude-plugin/marketplace.json`). This file is guidance for working **on** the
plugin. For what the plugin does for end users, see `README.md`.

## The golden rule — everything is English

- **Instructions are English.** Everything that instructs the model — `SKILL.md`, the agent bodies,
  the command bodies, the `reference/*.md`, and all YAML frontmatter — is English (Claude Code
  convention + portability).
- **Runtime user-facing output is English too.** Everything the plugin shows or writes at runtime —
  the agent's replies, the control panel, command effects, the hook's printed output, and the
  **content/values** written into `VENTURE.md` / `LANDSCAPE.md` — is English.
- **Structural headers are load-bearing.** `VENTURE.md` section headers (`Stage:`, `## Metrics source`,
  `## Kill line`, `## Decisions`, …) and the `Last scan:` line in `LANDSCAPE.md` stay exactly as
  written so the hook can parse them.

When in doubt: keep it English, and keep the structural headers verbatim.

## Repo layout

```
.claude-plugin/
  plugin.json          # manifest — name, version, author(OBJECT), keywords(ARRAY)
  marketplace.json     # makes this repo a single-plugin marketplace (plugin source "./")
skills/managing-microventures/
  SKILL.md             # orchestrator — MUST stay < 500 lines; push detail into reference/
  reference/*.md       # 9 files: protocol + per-gate + intake + methodology explainers
agents/*.md            # 9 lens/worker subagents
commands/*.md          # 5 slash commands: /start (kickoff) + audit/kill/override/details (overrides)
hooks/
  hooks.json           # SessionStart + Stop → check-state.py
  scripts/check-state.py
README.md  LICENSE  .gitignore
```

## Canonical model — keep it identical across ALL files

If you change any of these, grep the whole repo and change it **everywhere** (the most common bug is
drift between `SKILL.md`, `reference/`, the agents, the commands, and `README.md`):

- **9 lenses (emoji ↔ kebab name):** ⏳ keeper-of-time · 👾 tech-skeptic · 💼 business-pragmatist ·
  🕳 demand-scout · ⚔️ devils-advocate · 🃏 lateral · ⚖️ synthesizer · 🛰 landscape-watcher ·
  🧰 metrics-engineer.
- **4 gates + verdicts:** 0 Take it on? (`GO-INTO-SETUP`/`DROP`) · 1 Set the lines
  (`LINES-SET`/`LINES-INCOMPLETE`; output = written lines + named monkey) · 2 Checkpoint
  (`GO`/`PIVOT`/`KILL`/`SCALE`) · 3 Pivot (one single-element pivot, or `KILL`). **KILL & SCALE are
  verdicts of Gate 2, not gates.** 🃏 lateral sits on every gate.
- **Lens return block (≤6 lines):** `VERDICT` / `CONFIDENCE` 0–100% / `EVIDENCE` (2–3 facts+sources) /
  `KILL-TRIGGER WATCH`.
- **Course gradient (6 steps):** 🟢🟢 SCALE · 🟢 ON COURSE · 🟡 STALLING · 🟠 ALERT · 🔴 FAIL FAST ·
  ⚫ KILLED / 🏁 SHIPPED. Emoji belong to **Course**, never to **Stage**.
- **Stage values (bare):** SETUP → ALIVE → PIVOTING → SCALING → KILLED/SHIPPED.
- **VENTURE.md sections:** `# Venture`, `Stage:`, `Course:`, `Current gate:`, `## The bet`,
  `## Vacuum thesis`, `## Lean Canvas`, `## Success line`, `## Kill line`,
  `## Riskiest assumption (the monkey)`, `## Current experiment`, `## Metrics source`,
  `## Channels`, `## Log`, `## Decisions`.
- **Control panel:** the exact dashboard in `reference/venture-md-template.md` (§ Panel).

## Hard constraints when editing

- **`SKILL.md` < 500 lines.** Detail lives in `reference/`. Check with `wc -l`.
- **The hook must stay defensive.** `check-state.py` must never crash a session, never hard-block, and
  **always exit 0**. It stays silent when there is no `VENTURE.md`. SessionStart prints to **stdout**
  (injected as context); Stop emits JSON **`systemMessage`** (Stop stdout is NOT surfaced). `_read`
  accepts only regular files under a size cap (a FIFO / device / huge file must not stall it);
  `sys.stdout.reconfigure(utf-8)` so non-UTF-8 locales don't silently drop output. Re-run the smoke
  test after any change (see below).
- **Collector security invariant (do not weaken).** The metrics collector is project-local code, so it
  runs **only when `VENTURE.md` marks the source `✔ verified`** (opening a foreign repo with a
  collector must not execute it); with `cwd=project`, in its own process group (killed on timeout);
  its stdout is treated as untrusted (first line only, length-capped, control chars stripped) and
  **raw stderr is never echoed** into context.
- **Per-project state.** `VENTURE.md`, `LANDSCAPE.md`, and `scripts/metrics/` live at the **project
  root** of each venture — never in the plugin dir or home. The engine is global, the state is
  per-project.
- **Intake before record.** Gate 0/1 (and `/start`) interrogate the user, research claims, and pass
  the adequacy bar before writing a `VENTURE.md` line — never fill a line from a vague answer
  (`reference/intake-interview.md`). **Keep a single full path — no "lite" mode / behaviour
  branching** (deliberate product decision).
- **Secrets via env vars only** — never written into files (applies to generated metrics collectors).

## Authoring conventions (verified against code.claude.com/docs)

- `plugin.json`: `name` (kebab), `version` (semver), `author` is an **object** `{name,…}`,
  `keywords` is an **array**.
- Agent frontmatter: `name`, `description`, `tools` (comma list), `model: inherit`, `memory: project`.
  Tools per role: evidence lenses = `Read, Grep, Glob, WebSearch, WebFetch`; `synthesizer` read-only
  (`Read, Grep, Glob`); `landscape-watcher` +`Write, Edit`; `metrics-engineer` +`Write, Edit, Bash`.
- Command frontmatter: `description`, `argument-hint` (where useful); reference args via `$ARGUMENTS`.
- `hooks.json`: events `SessionStart` and `Stop` (exact case), `type: "command"`,
  `${CLAUDE_PLUGIN_ROOT}` for paths, a `timeout`. `${CLAUDE_PROJECT_DIR}` resolves the project root.

## Validate before every commit

```bash
claude plugin validate .                                  # manifest + marketplace
python3 -m json.tool .claude-plugin/plugin.json  >/dev/null
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
wc -l skills/managing-microventures/SKILL.md             # must be < 500
```

**Smoke-test the hook** in a throwaway dir (set `CLAUDE_PROJECT_DIR`). Cover: no `VENTURE.md` → silent;
full state → English status block; collector runs **only** when the source is `✔ verified` (and is NOT
executed otherwise); working / failing / **hanging** collector (timeout ~10s, no orphan procs);
collector output with control chars / multiple lines → sanitized to one clean line; a FIFO named
`VENTURE.md` → skipped, no hang; non-UTF-8 locale (`LANG=C`) → still prints; fresh / stale / garbled /
missing `LANDSCAPE.md`; `--on stop` complete → silent, incomplete or placeholder-only `## Decisions`
→ `systemMessage` listing the missing sections. It must always exit 0.

Also parse every YAML frontmatter (skill + agents + commands) before committing.

## Local install & release flow

This checkout is registered as a **directory marketplace** named `venture-compass` (user scope), so
edits to these files are picked up by **new** sessions automatically. After changing functional
content:

```bash
claude plugin marketplace update venture-compass            # refresh catalog
claude plugin update venture-compass@venture-compass        # bump installed version (restart to apply)
```

- Bump `version` in `plugin.json` for any functional change so the installed copy updates.
- Commit + push to `nnslvp/venture-compass` (branch `main`). **No `Co-Authored-By` lines** in commit
  messages.

## Self-check after edits

A consistency drift between files is the #1 defect class here. After non-trivial edits, grep the repo
for the lens names/emojis, the gate verdict words, "five/four gates", and the course-gradient emojis
to confirm nothing diverged; confirm the language split held.
