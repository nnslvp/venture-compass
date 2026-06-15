---
description: Close the current venture manually — confirm once (irreversible), record the verdict and the one lesson, point at the next bet.
argument-hint: "[reason for killing]"
---

Close the current venture **manually**, using the `managing-microventures` skill. KILL is
**irreversible**, so:

1. **Confirm once.** Show the kill line and ask plainly, in Russian: «Закрываем проект окончательно?
   Это необратимо. Да/нет». Proceed only on an explicit "да".
2. On confirmation, update `VENTURE.md`:
   - `Stage:` → `KILLED`
   - `Course:` → `⚫ KILLED`
   - Append to `## Decisions` (append-only): `<дата> · MANUAL · VERDICT: KILL (manual)` + the reason
     (`$ARGUMENTS` if given, else ask for one line) + **the one lesson** learned.
3. **Capture exactly one lesson** — the single most useful thing this bet taught.
4. **Point at the next bet** — one line on where the freed time/attention should go.
5. **Do not eulogize.** No long retrospective, no consolation. Killing on time is a win, not a
   failure. End with the panel showing `⚫ KILLED`.

A fired kill trigger that led here stays logged exactly as it fired — never rewrite it.
