#!/usr/bin/env python3
"""venture-compass state hook.

Defensive by design: it must NEVER crash a session and NEVER hard-block.
Everything is wrapped; the process always exits 0.

session-start -> prints a short Russian status block to stdout. Claude Code
                 injects SessionStart stdout into the session context, so this
                 is how prior state + live metrics + landscape staleness reach
                 the agent automatically each session.
stop          -> verifies VENTURE.md has the required sections and at least one
                 Decisions entry; if not, emits a JSON {"systemMessage": ...}
                 reminder (Stop stdout is NOT shown as context, so a plain print
                 would be invisible — systemMessage surfaces it to the user).

If VENTURE.md is absent, the hook stays completely silent so it never pollutes
unrelated projects where the plugin happens to be installed.
"""

import json
import os
import re
import signal
import subprocess
import sys
from datetime import date, datetime

LANDSCAPE_STALE_DAYS = 5
COLLECTOR_TIMEOUT = 10


def _project_dir():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def _read(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return None


def _today():
    return date.today()


def _field(text, name):
    """Value of a top-level `Name:` line (case-insensitive)."""
    if not text:
        return None
    m = re.search(r"^" + re.escape(name) + r"\s*:\s*(.+)$", text,
                  re.IGNORECASE | re.MULTILINE)
    return m.group(1).strip() if m else None


def _section(text, header):
    """Body of a `## Header ...` section up to the next `## ` or EOF."""
    if not text:
        return ""
    start_pat = re.compile(r"^##\s+" + re.escape(header) + r"\b.*$",
                           re.IGNORECASE | re.MULTILINE)
    m = start_pat.search(text)
    if not m:
        return ""
    nxt = re.compile(r"^##\s+", re.MULTILINE).search(text, m.end())
    return text[m.end():(nxt.start() if nxt else len(text))]


def _find_dates(text):
    out = []
    for token in re.findall(r"\d{4}-\d{2}-\d{2}", text or ""):
        try:
            out.append(datetime.strptime(token, "%Y-%m-%d").date())
        except Exception:
            pass
    return out


def _metrics_line(project):
    for name in ("collect.sh", "collect.py"):
        path = os.path.join(project, "scripts", "metrics", name)
        if not os.path.isfile(path):
            continue
        try:
            if name.endswith(".py"):
                cmd = [sys.executable or "python3", path]
            else:
                cmd = ["sh", path]
            # start_new_session isolates the collector in its own process group so a
            # backgrounded grandchild is killed on timeout instead of leaking and
            # holding the pipe open for the whole hook timeout.
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, start_new_session=True)
            try:
                out, err = proc.communicate(timeout=COLLECTOR_TIMEOUT)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except Exception:
                    proc.kill()
                try:
                    proc.communicate(timeout=2)
                except Exception:
                    pass
                return ("📊 Живые метрики: сборщик не ответил за " +
                        str(COLLECTOR_TIMEOUT) + "с — проверь scripts/metrics/" + name)
            if proc.returncode == 0 and (out or "").strip():
                return "📊 Живые метрики: " + out.strip().splitlines()[0]
            tail = ((err or "") + (out or "")).strip().splitlines()
            why = tail[0] if tail else ("код " + str(proc.returncode))
            return ("📊 Живые метрики: сборщик вернул ошибку (" + why +
                    ") — проверь scripts/metrics/" + name)
        except Exception as exc:
            return ("📊 Живые метрики: не удалось запустить сборщик (" +
                    type(exc).__name__ + ")")
    return ("📊 Источник метрик не настроен — запусти metrics-engineer, "
            "чтобы цифры не брались «со слов»")


def _landscape_line(project):
    text = _read(os.path.join(project, "LANDSCAPE.md"))
    if text is None:
        return "🛰 LANDSCAPE.md нет — пора пройтись по внешнему ландшафту (landscape-watcher)"
    m = re.search(r"^(?:Last scan|Последнее сканирование)\s*:\s*(\d{4}-\d{2}-\d{2})",
                  text, re.IGNORECASE | re.MULTILINE)
    if not m:
        return "🛰 LANDSCAPE.md без даты сканирования — обнови ландшафт (landscape-watcher)"
    try:
        scan = datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except Exception:
        return "🛰 LANDSCAPE.md: дата сканирования нечитаема — обнови ландшафт (landscape-watcher)"
    age = (_today() - scan).days
    if age > LANDSCAPE_STALE_DAYS:
        return ("🛰 Ландшафт устарел (" + str(age) +
                " дн. назад) — обнови (landscape-watcher)")
    return None


def on_session_start(project, text):
    out = ["🎛 venture-compass — состояние проекта"]
    nm = re.search(r"^#\s*Venture\s*:?\s*(.+)$", text, re.IGNORECASE | re.MULTILINE)
    if nm and nm.group(1).strip():
        out[0] = "🎛 venture-compass — " + nm.group(1).strip()
    for label, key in (("Этап", "Stage"), ("Курс", "Course"), ("Ворота", "Current gate")):
        val = _field(text, key)
        if val:
            out.append(label + ": " + val)

    dates = sorted(_find_dates(_section(text, "Kill line")))
    if dates:
        today = _today()
        upcoming = [d for d in dates if d >= today]
        nearest = upcoming[0] if upcoming else dates[-1]
        days = (nearest - today).days
        if days >= 0:
            out.append("💀 Ближайший киллтриггер: " + nearest.isoformat() +
                       " (через " + str(days) + " дн.)")
        else:
            out.append("💀 Киллтриггер ПРОСРОЧЕН: " + nearest.isoformat() +
                       " (" + str(-days) + " дн. назад) — пора на чекпоинт")

    out.append(_metrics_line(project))
    landscape = _landscape_line(project)
    if landscape:
        out.append(landscape)
    print("\n".join(out))


def on_stop(project, text):
    missing = []
    if not re.search(r"^Stage\s*:", text, re.IGNORECASE | re.MULTILINE):
        missing.append("Stage:")
    if not re.search(r"^##\s+Kill line\b", text, re.IGNORECASE | re.MULTILINE):
        missing.append("## Kill line")
    if not re.search(r"^##\s+Decisions\b", text, re.IGNORECASE | re.MULTILINE):
        missing.append("## Decisions")
    else:
        body = _section(text, "Decisions")
        has_entry = bool(re.search(r"^\s*[-*0-9]|VERDICT|ВЕРДИКТ", body or "",
                                   re.IGNORECASE | re.MULTILINE))
        if not has_entry:
            missing.append("запись в ## Decisions")
    if missing:
        msg = ("⚠ VENTURE.md неполон: нет " + ", ".join(missing) +
               ". Ворота не закрыты, пока вердикт и оценки линз не записаны в ## Decisions.")
        try:
            print(json.dumps({"systemMessage": msg}, ensure_ascii=False))
        except Exception:
            pass


def main():
    try:
        argv = sys.argv[1:]
        mode = "session-start"
        if "--on" in argv:
            i = argv.index("--on")
            if i + 1 < len(argv):
                mode = argv[i + 1]
        project = _project_dir()
        text = _read(os.path.join(project, "VENTURE.md"))
        if text is None:
            return  # not a venture project — stay silent
        if mode == "stop":
            on_stop(project, text)
        else:
            on_session_start(project, text)
    except Exception:
        pass  # never crash a session


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
