---
description: Kick off a new micro-venture in this project — scaffold the base files automatically, then run the guided intake interview (Gate 0 → Gate 1) and fill VENTURE.md. The init / start command.
argument-hint: "[idea in one sentence]"
---

Initialize and kick off a micro-venture in the **current project folder**, using the
`managing-microventures` skill. This is the guided entry point: first scaffold state, then interrogate
the user to fill it. Everything written goes to the **project root** (one set per venture).

## 1. Scaffold the base files (automatic, idempotent — never clobber)

Run this with the **Bash** tool in the project root. It creates the state files and wires `CLAUDE.md`
without overwriting anything that already exists:

```bash
[ -f VENTURE.md ] || cat > VENTURE.md <<'EOF'
# Venture: <name>

Stage: SETUP
Course: 🟢 ON COURSE
Current gate: 0 · Take it on?

## The bet
<what we're betting on and why now>
## Vacuum thesis
<what vacuum; a real demand signal — NOT "no competitors">
## Lean Canvas
Version: v1
## Success line
<state + date>
## Kill line
- <trigger 1: state + date>
- <trigger 2: state + date>
Honest P(success): <~%>
## Riskiest assumption (the monkey)
<the most lethal assumption; tested first>
## Current experiment
- Hypothesis: <...>
- What we measure (OMTM): <...>
- Decision date: <date>
- Cost cap: <...>
## Metrics source
Type: none
Status: ⚠ self-reported
## Channels
<...>
## Log
- start
## Decisions
<!-- append-only: gate · VERDICT · each lens's call · why -->
EOF
grep -q '@VENTURE.md' CLAUDE.md 2>/dev/null || printf '\n@VENTURE.md\n@LANDSCAPE.md\n' >> CLAUDE.md
[ -f LANDSCAPE.md ] || printf 'Last scan: %s\n\n## Moves a trigger ⚠️\n- none\n' "$(date +%F)" > LANDSCAPE.md
echo "scaffold ok"
```

If `VENTURE.md` already exists with **real** (non-placeholder) content, do NOT re-scaffold — tell the
user the venture already exists and offer `/audit` (checkpoint) or to resume instead.

## 2. Run the guided intake — ask all the questions

Then immediately run the intake interview from `reference/intake-interview.md` (full protocol):

- **Gate 0 · Take it on?** — interrogate for the bet, the vacuum + a real demand signal, platform
  risk, and constraints; research each checkable claim; verdict **GO-INTO-SETUP** / **DROP**.
- On GO, **Gate 1 · Set the lines** — drill out every field: success line, ≥2 dated kill triggers,
  honest P%, the monkey, the first experiment, the metrics source, channels.

Discipline: **ask one thread at a time**; refuse vague / hypothetical / wishlist answers (The Mom
Test); research claims and confront the user with what you find; sanity-check every goal for adequacy.
Fill the `<...>` placeholders in `VENTURE.md` as concrete, checked answers land. If `$ARGUMENTS` is
given, seed "the bet" with it and start drilling from there.

## 3. Finish

When the lines are concrete and adequacy-passed: set `Stage:` → `ALIVE`, log Gate 0/1 to
`## Decisions` (verdict + each lens's call + why), offer to wire the metrics source via
`metrics-engineer`, and print the control panel. Irreversible calls (KILL / committing a PIVOT) are
proposed and wait for the user's explicit "yes".
