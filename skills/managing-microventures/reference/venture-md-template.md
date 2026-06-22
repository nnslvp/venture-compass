# VENTURE.md template + control panel

`VENTURE.md` is the single source of truth for one micro-venture. It must let a fresh session weeks
later resume with **zero re-interrogation**.

**Language rule:** everything — content and structure — is **English**. The structural headers below
stay exactly as written so the SessionStart/Stop hook can parse them. Keep `Stage:`, `Course:`,
`Current gate:`, `## Metrics source`, `## Kill line`, `## Decisions` verbatim.

---

## Stage values (the `Stage:` line)

`SETUP → ALIVE → PIVOTING → SCALING → KILLED/SHIPPED`

## Course gradient (the `Course:` line — 6 steps)

| Step | Meaning |
|------|---------|
| `🟢🟢 SCALE` | success line met — time to pour fuel on |
| `🟢 ON COURSE` | moving, target reachable, no trigger near |
| `🟡 STALLING` | drift — activity but flat OMTM |
| `🟠 ALERT` | a kill trigger is within one checkpoint of firing |
| `🔴 FAIL FAST` | a kill trigger has fired |
| `⚫ KILLED` / `🏁 SHIPPED` | closed |

---

## Section template

Copy this skeleton into the project's `VENTURE.md` (at the **project root**, one per venture). Fill
the `<...>` in English.

```markdown
# Venture: <name>

Stage: <ALIVE>
Course: <🟢 ON COURSE>
Current gate: <2 · Checkpoint>

## The bet
<One or two lines: what we're betting on and why now. The essence.>

## Vacuum thesis
<What vacuum we're filling. MANDATORY: a real demand signal — search queries,
communities, complaints, workarounds, willingness to pay/show up. NOT "no competitors".>

## Lean Canvas
Version: <v1 · 2026-06-15>
- Problem: <...>
- Segment: <...>
- UVP: <...>
- Solution: <...>
- Channels: <...>
- Revenue / value stream: <...>
- Costs: <...>
- Metrics: <...>
- Unfair advantage: <...>
<Riskiest assumption — mark it ⚠ and carry it into the "the monkey" section below.>

## Success line
<State + date: "by 2026-07-15 — 200 weekly actives".>

## Kill line
- Trigger 1 (state + date): <"by 2026-06-30 fewer than 50 actives">.
- Trigger 2 (state + date): <"none of the 3 channels hit CAC < value by 2026-07-10">.
Honest P(success) today: <~25%>.

## Riskiest assumption (the monkey)
<The most lethal unproven assumption. What we test FIRST and how.>

## Current experiment
- Hypothesis: <...>
- What we measure (OMTM): <...>
- Decision date: <2026-06-30>
- Cost cap (time/money): <...>

## Metrics source
Type: <script | file | API | none>
Where: <scripts/metrics/collect.sh | path to export | endpoint>
Last live read: <2026-06-15 = 17>
Status: <✔ verified | ⚠ self-reported>

## Channels
<Bullseye: list of tested channels and the result of each.>

## Log
- <2026-06-15> — <what we did>.

## Decisions
<!-- append-only. Every gate: gate · VERDICT · each lens's call · why.
KILL/PIVOT are marked proposed, then confirmed after the user's "yes". -->
- <2026-06-15> · Gate 1 · VERDICT: LINES-SET · lenses: ⚔️ ⏳ 💼 🃏 · why: <...>.
```

---

## Panel (control panel)

Print this dashboard **at the end of every substantive reply**, so the kill line stays in view. It is
a glanceable status, **not** a "copy this" block. The gauge dot `●` shows the OMTM's position between
the KILL threshold (left) and the target 🎯 (right).

```
🎛 VENTURE PANEL
Venture:  <name / essence>
Stage:    <ALIVE>  ·  Gate: <current>
Course:   <🟠 ALERT>   💀 KILL ───●──────── 🎯   (<% to target> · <days to trigger>)
🎯 Vector:  <current experiment> → decision <date>
💀 Trigger: <what will kill us and by when>
📊 OMTM:    <metric> = <current> / <target>   <✔ freshness: today | ⚠ self-reported>
Latest:   <what we did just now>
```

Filled example:

```
🎛 VENTURE PANEL
Venture:  HazeBot — auto-cut Reels from streams
Stage:    ALIVE  ·  Gate: 2 · Checkpoint
Course:   🟠 ALERT   💀 KILL ──●───────── 🎯   (34% to target · 5 days to trigger)
🎯 Vector:  paid test of 3 channels → decision 2026-06-20
💀 Trigger: <50 actives by 2026-06-20
📊 OMTM:    actives/week = 17 / 50   ✔ freshness: today
Latest:   shipped TikTok autoposting
```

The gauge dot moves left as the OMTM nears the KILL threshold and right as it nears the target. When
the OMTM is at or below KILL: `💀●─────────── 🎯` and Course flips to `🔴 FAIL FAST`.

---

## Project CLAUDE.md (auto-wire)

During Gate 1 setup, create the venture's `CLAUDE.md` at the project root (or **append** to an
existing one — **never clobber**) so the state auto-loads each session and survives `/compact`. Create
`VENTURE.md` first so the `@`-import isn't dangling. Content in English:

```markdown
# <Venture name>

This project is run through venture-compass (a micro-venture).

@VENTURE.md
@LANDSCAPE.md

At the start of every session, silently reconstruct context from VENTURE.md and LANDSCAPE.md and give
a briefing (where we are → what changed outside → what it means → recommendation) + the panel. Then
drive the cycle yourself: watch the dates / metrics / landscape, run checkpoints on your own, and on a
fired kill trigger recommend KILL and wait for an explicit "yes".
```
