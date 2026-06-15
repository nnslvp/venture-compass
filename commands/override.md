---
description: Reject or hold the agent's last call — logged as an OVERRIDE, never erasing a fired trigger or silently moving a line.
argument-hint: "[what to change or hold]"
---

The user is overriding your **last call**, using the `managing-microventures` skill.

1. **Acknowledge in one line** (Russian) — no argument, no defensiveness.
2. **Log it** in `VENTURE.md → ## Decisions` (append-only): `<дата> · OVERRIDE · <что отклонено/на
   удержании> · по запросу пользователя`. Reference `$ARGUMENTS`.
3. **Adjust as directed** — pause the gate, hold the verdict, or re-weight as the user asks.

Hard limits (state them if the user's request crosses one):
- A **fired kill trigger is never erased or rewritten** — it stays in the log exactly as it fired.
- A success/kill **line is never silently moved.** Changing criteria is allowed only as a
  **deliberate, separately-logged decision** (`<дата> · CRITERIA-CHANGE · old → new · why`), not as a
  quiet goalpost shift to keep the bet alive.

End with the updated panel.
