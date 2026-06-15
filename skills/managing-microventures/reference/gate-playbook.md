# Gate playbook — per-gate detail

The Stage-Gate spine (Cooper). Four numbered gates; **KILL and SCALE are verdicts of Gate 2**, not
separate gates. The 🃏 lateral seat sits on **every** gate, barred from the obvious framings. For the
shared blind-panel mechanics see `consilium-protocol.md`.

---

## Gate 0 · Браться ли

**Fires:** a raw idea, before any setup.
**Question for the brief:** is there a real, reachable vacuum worth a small bet — or should we drop it
now and save the time?
**Lenses:** 🕳 demand-scout · 👾 tech-skeptic · ⚔️ devils-advocate · 🃏 lateral.
**Verdict vocabulary:** `GO-INTO-SETUP` / `DROP`.

**Intake first:** interrogate the user for the demand/feasibility fields (the bet, the vacuum + a real
demand signal, platform risk, constraints) — drill, research each claim, refuse mush
(`intake-interview.md`). Don't issue GO/DROP until the inputs are concrete.

**Emphasis:**
- 🕳 demand-scout runs The Mom Test on the demand: past behavior and commitments, not "would you use
  it?". Demands a real signal; **"no competitors" is not a signal** — a dead market also has no
  competitors.
- 👾 tech-skeptic checks platform / "rented land" risk and whether a solo-with-AI builder can ship and
  maintain it.
- ⚔️ devils-advocate argues the strongest case to DROP.
- 🃏 lateral looks for a sideways form (SDK to incumbents instead of an app; B2B flip; reuse existing
  infra; 1000-true-fans niche).

**Borrowed:** The Mom Test; low-comp-vs-dead; platform risk; 1000 True Fans.
**On GO-INTO-SETUP:** Stage → `SETUP`; open Gate 1. Write the verdict + lens calls to `## Decisions`.

---

## Gate 1 · Сетап линий

**Fires:** setting up the venture — fixing the success and kill criteria *before* building.
**Question for the brief:** what exactly, by when, means this worked — and what means it's dead? What
is the one riskiest assumption?
**Lenses:** ⚔️ devils-advocate (pre-mortem) · ⏳ keeper-of-time · 💼 business-pragmatist · 🃏 lateral.
**Output (not a GO/KILL verdict):** the **written lines** (success line, ≥2 kill triggers, honest P%)
+ the **named monkey** (riskiest assumption), recorded in `VENTURE.md`.

**Intake first:** run the full intake interview (`intake-interview.md`) — squeeze out every field
(success line, ≥2 kill triggers, honest P%, the monkey, the first experiment, the metrics source,
channels, constraints), research the checkable claims, and sanity-check each for adequacy before you
write the lines.

**Emphasis:**
- ⚔️ devils-advocate runs a **pre-mortem** ("it's 6 months later and this failed — why?") and converts
  the top reasons into **state+date** kill triggers.
- ⏳ keeper-of-time makes every line **measurable and dated** — no vague "get traction".
- 💼 business-pragmatist writes a **reverse income statement** / cost-per-engaged-user and an
  opportunity-cost view.
- 🃏 lateral checks the lines aren't quietly assuming the obvious shape is the only one.
- Identify the **monkey** (monkeys & pedestals) and make the first experiment test it **first**.

**Borrowed:** Lean Canvas riskiest-first; pre-mortem; state+date kill criteria; reverse income
statement; monkeys & pedestals.
**On completion:** Stage → `ALIVE`; lines written; first experiment defined; **wire the project
`CLAUDE.md`** (create, or append to it — `@VENTURE.md` + `@LANDSCAPE.md`, never clobber); log to
`## Decisions`.

---

## Gate 2 · Чекпоинт

**Fires (you trigger it yourself):** a kill/success date hits · a metric breaches a threshold · drift
(activity but flat OMTM) · on request (`/audit`).
**Question for the brief:** against the lines **as written**, is this GO, PIVOT, KILL or SCALE?
**Lenses:** ⏳ · 👾 · 💼 · 🕳 · ⚔️ as the **Жизнь vs Смерть** pair (Адвокат смерти + Адвокат жизни) · 🃏.
**Verdict vocabulary:** `GO` / `PIVOT` / `KILL` / `SCALE`.

**Always pull live metrics first** from `## Источник метрик` — never judge on a self-reported number.

**Emphasis:**
- ⏳ keeper-of-time compares the actual metric to the lines **exactly as written** (no goalpost-moving),
  hunts drift, checks the monkey was tested first, weighs opportunity cost; on the fence at a fired
  trigger → KILL.
- 💼 business-pragmatist: OMTM vs threshold (not vanity), unit economics (CAC < LTV, or
  cost-per-engaged-user for non-monetary), reverse income statement.
- 🕳 demand-scout: is the vacuum filling fast (closing window)? do Bullseye channels work? non-monetary
  demand still real?
- 👾 tech-skeptic: did the technical assumption hold in the field? hidden hacks / maintenance burden?
- ⚔️ pair: strongest KILL case vs strongest honest CONTINUE case, independent; synthesizer picks the
  stronger blind of preference.

**Borrowed:** Build-Measure-Learn; AARRR + OMTM; Bullseye; innovation accounting.

**Verdict handling:**
- `GO` — keep course; maybe sharpen the next experiment. Reversible → issue yourself.
- `SCALE` — success line met; Stage → `SCALING`, Course → `🟢🟢 SCALE`; define the scale experiment.
- `PIVOT` — open Gate 3. Committing the pivot is irreversible → **propose, then confirm**.
- `KILL` — a fired trigger; recommend KILL hard, don't soften. Irreversible → **propose, then
  confirm**. On confirm: Stage → `KILLED`, Course → `⚫ KILLED`, capture the one lesson, point at the next bet.

---

## Gate 3 · Пивот

**Fires:** Gate 2 returned PIVOT.
**Question for the brief:** which single element change best fits the evidence — or is there no honest
pivot (→ KILL)?
**Lenses:** 4 ephemeral generators (audience / problem / solution / channel) + 🃏, all judged blind.
**Verdict:** one **single-element** pivot, or `KILL`.

**Mechanic (Dialectical Inquiry + Analysis of Competing Hypotheses):** each generator produces the
*best* pivot for its element; the synthesizer picks the best-fitting one or declares "no honest pivot
→ KILL". **Change exactly one element; keep the learning** accumulated so far.

**Borrowed:** Dialectical Inquiry; Analysis of Competing Hypotheses.
**On a committed pivot (after confirm):** Stage → `PIVOTING`, update the Lean Canvas snapshot (new
version), reset the success/kill lines and the experiment for the new bet, log to `## Decisions`.
