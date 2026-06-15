# VENTURE.md template + control panel

`VENTURE.md` is the single source of truth for one micro-venture. It must let a fresh session weeks
later resume with **zero re-interrogation**.

**Language rule:** the *content* (every value, note, log line) is written in **Russian**. The
structural headers below stay exactly as written (English, except `## Источник метрик`) so the
SessionStart/Stop hook can parse them. Keep `Stage:`, `Course:`, `Current gate:`, `## Kill line`,
`## Decisions` verbatim.

---

## Stage values (the `Stage:` line)

`SETUP → ALIVE → PIVOTING → SCALING → KILLED/SHIPPED`

## Course gradient (the `Course:` line — 6 steps)

| Step | Meaning |
|------|---------|
| `🟢🟢 SCALE` | success line met — time to pour fuel on |
| `🟢 НА КУРСЕ` | moving, target reachable, no trigger near |
| `🟡 БУКСУЕМ` | drift — activity but flat OMTM |
| `🟠 ТРЕВОГА` | a kill trigger is within one checkpoint of firing |
| `🔴 FAIL FAST` | a kill trigger has fired |
| `⚫ KILLED` / `🏁 SHIPPED` | closed |

---

## Section template

Copy this skeleton into the project's `VENTURE.md` (at the **project root**, one per venture). Fill
the `<...>` in Russian.

```markdown
# Venture: <название>

Stage: <ALIVE>
Course: <🟢 НА КУРСЕ>
Current gate: <2 · Чекпоинт>

## The bet
<Одна-две строки: на что ставим и почему сейчас. Самая суть.>

## Vacuum thesis
<Какой вакуум закрываем. ОБЯЗАТЕЛЬНО сигнал реального спроса — поисковые запросы,
сообщества, жалобы, обходные решения, готовность платить/приходить. НЕ «нет конкурентов».>

## Lean Canvas
Версия: <v1 · 2026-06-15>
- Проблема: <...>
- Сегмент: <...>
- УТП: <...>
- Решение: <...>
- Каналы: <...>
- Поток дохода / ценности: <...>
- Издержки: <...>
- Метрики: <...>
- Несправедливое преимущество: <...>
<Самое рискованное допущение — пометить ⚠ и вынести в раздел «the monkey» ниже.>

## Success line
<Состояние + дата: «к 2026-07-15 — 200 активных в неделю».>

## Kill line
- Триггер 1 (состояние + дата): <«к 2026-06-30 меньше 50 активных»>.
- Триггер 2 (состояние + дата): <«ни один из 3 каналов не дал CAC < ценности к 2026-07-10»>.
Честная P(успеха) на сегодня: <~25%>.

## Riskiest assumption (the monkey)
<Самое смертельное недоказанное допущение. Что проверяем ПЕРВЫМ и как.>

## Current experiment
- Гипотеза: <...>
- Что меряем (OMTM): <...>
- Дата решения: <2026-06-30>
- Потолок затрат (времени/денег): <...>

## Источник метрик
Тип: <script | file | API | none>
Где: <scripts/metrics/collect.sh | путь к экспорту | эндпоинт>
Последнее живое чтение: <2026-06-15 = 17>
Статус: <✔ verified | ⚠ self-reported>

## Channels
<Bullseye: список протестированных каналов и результат каждого.>

## Log
- <2026-06-15> — <что сделали>.

## Decisions
<!-- append-only. Каждые ворота: ворота · VERDICT · оценка каждой линзы · почему.
KILL/PIVOT помечаются proposed, затем confirmed после «да» пользователя. -->
- <2026-06-15> · Gate 1 · VERDICT: LINES-SET · линзы: ⚔️ ⏳ 💼 🃏 · why: <...>.
```

---

## Панель (control panel)

Print this dashboard **in Russian at the end of every substantive reply**, so the kill line stays in
view. It is a glanceable status, **not** a "copy this" block. The gauge dot `●` shows the OMTM's
position between the KILL threshold (left) and the target 🎯 (right).

```
🎛 ПАНЕЛЬ ПРОЕКТА
Проект:  <название / суть>
Этап:    <ALIVE>  ·  Ворота: <текущие>
Курс:    <🟠 ТРЕВОГА>   💀 KILL ───●──────── 🎯   (<% к цели> · <дней до триггера>)
🎯 Вектор:  <текущий эксперимент> → решение <дата>
💀 Триггер: <что и к какой дате нас убьёт>
📊 OMTM:    <метрика> = <текущее> / <цель>   <✔ свежесть: сегодня | ⚠ со слов>
Последнее:  <что сделали сейчас>
```

Filled example:

```
🎛 ПАНЕЛЬ ПРОЕКТА
Проект:  ДымкаBot — авто-нарезка Reels из стримов
Этап:    ALIVE  ·  Ворота: 2 · Чекпоинт
Курс:    🟠 ТРЕВОГА   💀 KILL ──●───────── 🎯   (34% к цели · 5 дней до триггера)
🎯 Вектор:  платный тест 3 каналов → решение 2026-06-20
💀 Триггер: <50 активных к 2026-06-20
📊 OMTM:    активных/нед = 17 / 50   ✔ свежесть: сегодня
Последнее:  выкатили автопостинг в TikTok
```

The gauge dot moves left as the OMTM nears the KILL threshold and right as it nears the target. When
the OMTM is at or below KILL: `💀●─────────── 🎯` and Course flips to `🔴 FAIL FAST`.
