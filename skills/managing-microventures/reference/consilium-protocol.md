# Consilium protocol — the blind adversarial panel

The consilium is **real, not theater.** Its whole point is **independence**: lenses judge blind, in
their own contexts, off one identical neutral brief, and only then does a synthesizer fuse them. This
is Dialectical Inquiry / Devil's Advocacy (Schweiger, Sandberg & Ragan, *AMJ* 1986) + the Mediating
Assessments Protocol (Kahneman, *Noise*) + the anti-groupthink rule (judge independently first,
synthesize second — Asch / Janis).

Run the whole thing **inside**; surface only the short result (see step 6).

---

## Step 1 — Neutral brief

Build one brief from `VENTURE.md`. **Facts only.** Identical for every lens. No hint of a preferred
outcome. **No lens names** and no mention that other lenses exist.

Brief skeleton (fill from `VENTURE.md`, in Russian):

```
ПРОЕКТ: <суть>
СТАВКА: <the bet>
ВАКУУМ + СИГНАЛ СПРОСА: <vacuum thesis + evidence>
ЛИНИЯ УСПЕХА (как записана): <state+date>
ЛИНИЯ СМЕРТИ (как записана): <triggers + P%>
САМОЕ РИСКОВАННОЕ ДОПУЩЕНИЕ: <the monkey>
ТЕКУЩИЙ ЭКСПЕРИМЕНТ: <hypothesis, measure, decision date, cap>
ЖИВЫЕ МЕТРИКИ (из источника, не «со слов»): <OMTM = current / target · freshness>
КАНАЛЫ: <bullseye state>
ВОПРОС ВОРОТ: <the one decision this gate must make>
```

Never embed your own opinion. If a number is self-reported (not verified live), label it so — the
lenses must know the evidence is soft.

---

## Step 2 — Blind parallel dispatch

Spawn the gate's lenses as **separate subagents in the same turn** (parallel), each receiving only
the brief. None sees the others' work. Each lens **gathers fresh evidence** — web search, read
state/code — it judges off reality, not priors.

Each lens returns a **≤6-line block**:

```
VERDICT: <gate vocabulary — e.g. GO / PIVOT / KILL / SCALE / DROP / GO-INTO-SETUP>
CONFIDENCE: <0–100%>
EVIDENCE:
- <fact + source>
- <fact + source>
KILL-TRIGGER WATCH: <which trigger this moves · met | imminent | far>
```

Which lenses per gate: see `gate-playbook.md`. The 🃏 lateral seat is on every gate.

---

## Step 3 — Collect + seek the disconfirming case

Gather all blocks. Then apply **Analysis of Competing Hypotheses discipline**: actively try to
**disprove** the currently-favored direction, not confirm it. **One hard disconfirming fact outweighs
several soft confirmations.** If every lens agrees, be suspicious — look for what they all missed
(send a fresh probe or a Delphi round before trusting unanimity).

---

## Step 4 — Synthesis (Mediating Assessments Protocol)

Hand all blocks to the **⚖️ synthesizer** (read-only). It:

1. Reviews each assessment **on its own** first (no averaging yet, no anchoring on the loudest).
2. Weighs each against the **lines as written** — **no goalpost-moving**. The success/kill lines are
   what they were when set; do not quietly relax them to keep the project alive.
3. Makes **one delayed holistic verdict** only after all assessments are reviewed.
4. **Tie-break:** at a fired kill trigger, break toward **KILL** (small-bet asymmetry — the cost of
   continuing a dead bet exceeds the cost of killing a live one too early).
5. Gives the disconfirming fact its weight; names any overruled lens **with the fact that justifies
   overruling it**.

Synthesizer output: `VERDICT · WHY (2–4 lines) · NEXT · DELPHI? (y/n)`.

---

## Step 5 — Delphi round on sharp conflict

If lenses sharply conflict (or the synthesizer flags `DELPHI? y`): feed the **anonymized** spread of
verdicts/confidences back to the lenses **once**, let each revise, then re-synthesize. Stop when
stable. **≤2 rounds.** If the panel keeps flip-flopping, the question is **underspecified** — stop and
ask the user for the one missing fact rather than spinning.

---

## Step 6 — Log, then surface

1. **Log** to `VENTURE.md → ## Decisions` (append-only): the gate, the **VERDICT**, **each lens's
   call**, and the why. Irreversible verdicts (KILL, committing a PIVOT) written as **proposed**.
2. **Surface** to the user only: **verdict + 2–4 reasons + the panel.** ~6 lines.
3. **Hold** all transcripts. Reveal them only on `/details`.
4. The gate is **closed** only once the log entry exists. Irreversible verdicts flip to **confirmed**
   only after the user's explicit "да".

---

## Gate 2 — the «Жизнь vs Смерть» dialectical pair

On a checkpoint, run ⚔️ devils-advocate **twice**, as two independent subagents:

- **Адвокат смерти** — build the strongest evidence-backed case to **KILL**.
- **Адвокат жизни** — build the strongest *honest* case to **CONTINUE** (no cheerleading, no
  goalpost-moving; real evidence only).

Each is blind to the other. The synthesizer picks the stronger case **blind of preference** — it must
not default to "continue" out of momentum.

---

## Gate 3 — four ephemeral pivot generators

When Gate 2 returns PIVOT, spawn **four ephemeral generator subagents**, one per Lean-Canvas element,
each producing the **best single-element pivot**:

- **audience** — keep everything, change *who* it's for.
- **problem** — same audience, attack a *different problem* they have.
- **solution** — same problem, a *different form* of solution.
- **channel** — same product, a *different way to reach* people.

Add 🃏 lateral. Judge all blind. The synthesizer picks the best by fit to the evidence, or concludes
"no honest pivot → KILL". **Change exactly one element; keep the learning** carried so far.
