#!/usr/bin/env python3
"""venture-compass state hook.

Defensive by design: it must NEVER crash a session and NEVER hard-block.
Everything is wrapped; the process always exits 0.

session-start -> prints a short Russian status block to stdout. Claude Code
                 injects SessionStart stdout into the session context, so this
                 is how prior state + live metrics + landscape staleness reach
                 the agent automatically each session.
stop          -> verifies VENTURE.md has the required sections and at least one
                 REAL Decisions entry; if not, emits a JSON {"systemMessage": ...}
                 reminder (Stop stdout is NOT shown as context, so a plain print
                 would be invisible — systemMessage surfaces it to the user).

Security: the metrics collector under scripts/metrics/ is project-local code, so
it is treated as untrusted. It runs ONLY when VENTURE.md marks the metrics source
"✔ verified" — opening some other repo that merely contains a collector does not
execute it. Its output is treated as untrusted too: one line, length-capped,
control characters stripped; raw stderr is never echoed into the model context.

If VENTURE.md is absent, the hook stays completely silent so it never pollutes
unrelated projects where the plugin happens to be installed.
"""

import json
import os
import re
import signal
import stat
import subprocess
import sys
from datetime import date, datetime

LANDSCAPE_STALE_DAYS = 5
COLLECTOR_TIMEOUT = 10
MAX_FILE_BYTES = 1_000_000
MAX_METRIC_CHARS = 200

# Decision-critical sections that let a fresh session reconstruct the venture.
REQUIRED_SECTIONS = [
    ("Stage:", r"^Stage\s*:"),
    ("Course:", r"^Course\s*:"),
    ("Current gate:", r"^Current gate\s*:"),
    ("## The bet", r"^##\s+The bet\b"),
    ("## Vacuum thesis", r"^##\s+Vacuum thesis\b"),
    ("## Success line", r"^##\s+Success line\b"),
    ("## Kill line", r"^##\s+Kill line\b"),
    ("## Riskiest assumption", r"^##\s+Riskiest assumption\b"),
    ("## Current experiment", r"^##\s+Current experiment\b"),
    ("## Источник метрик", r"^##\s+Источник метрик"),
    ("## Decisions", r"^##\s+Decisions\b"),
]


def _project_dir():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def _read(path):
    """Read a regular text file, size-capped. Skip FIFOs/devices/huge files so a
    crafted path can never stall the 'never block' contract."""
    try:
        st = os.stat(path)
        if not stat.S_ISREG(st.st_mode):
            return None
        if st.st_size > MAX_FILE_BYTES:
            return None
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read(MAX_FILE_BYTES)
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


def _clean_metric(s):
    """Treat collector stdout as untrusted: first non-empty line, control chars
    stripped (no ANSI / prompt-injection), length-capped."""
    raw = (s or "").strip()
    line = raw.splitlines()[0] if raw else ""
    line = "".join(ch for ch in line if ch == " " or ch.isprintable())
    if len(line) > MAX_METRIC_CHARS:
        line = line[:MAX_METRIC_CHARS] + "…"
    return line.strip()


def _source_verified(text):
    """True only if the metrics source is explicitly marked '✔ verified'."""
    return bool(re.search(r"✔\s*verified", _section(text, "Источник метрик"),
                          re.IGNORECASE))


def _kill_pg(pgid):
    if pgid is None:
        return
    try:
        os.killpg(pgid, signal.SIGKILL)
    except Exception:
        pass


def _metrics_line(project, text):
    collector = None
    for name in ("collect.sh", "collect.py"):
        path = os.path.join(project, "scripts", "metrics", name)
        if os.path.isfile(path):
            collector = (name, path)
            break
    if not collector:
        return ("📊 Источник метрик не настроен — запусти metrics-engineer, "
                "чтобы цифры не брались «со слов»")
    name, path = collector
    if not _source_verified(text):
        return ("📊 Коллектор есть, но источник не помечен «✔ verified» в "
                "## Источник метрик — не запускаю из соображений доверия "
                "(прогони metrics-engineer и подтверди источник)")

    proc = None
    pgid = None
    try:
        cmd = [sys.executable or "python3", path] if name.endswith(".py") else ["sh", path]
        # Own session/process group (so a backgrounded grandchild can be killed)
        # and cwd at the project root (so the collector's relative paths resolve).
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True, cwd=project)
        try:
            pgid = os.getpgid(proc.pid)
        except Exception:
            pgid = None
        try:
            out, _err = proc.communicate(timeout=COLLECTOR_TIMEOUT)
        except subprocess.TimeoutExpired:
            _kill_pg(pgid)
            try:
                proc.communicate(timeout=2)
            except Exception:
                pass
            return ("📊 Живые метрики: сборщик не ответил за " +
                    str(COLLECTOR_TIMEOUT) + "с — проверь scripts/metrics/" + name)
        if proc.returncode == 0:
            metric = _clean_metric(out)
            if metric:
                return "📊 Живые метрики: " + metric
            return ("📊 Живые метрики: сборщик ничего не вернул — "
                    "проверь scripts/metrics/" + name)
        # Never echo raw stderr (may carry secrets or model-context injection).
        return ("📊 Живые метрики: сборщик вернул ошибку (код " +
                str(proc.returncode) + ") — проверь scripts/metrics/" + name)
    except Exception as exc:
        return ("📊 Живые метрики: не удалось запустить сборщик (" +
                type(exc).__name__ + ")")
    finally:
        # Only if the leader is still alive — avoids killing a reused pgid.
        try:
            if proc is not None and proc.poll() is None:
                _kill_pg(pgid)
        except Exception:
            pass


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

    out.append(_metrics_line(project, text))
    landscape = _landscape_line(project)
    if landscape:
        out.append(landscape)
    print("\n".join(out))


def _has_real_decision(body):
    """A real entry has VERDICT/ВЕРДИКТ and a BARE date — not a `<YYYY-MM-DD>`
    placeholder or an HTML comment."""
    if not body:
        return False
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("<!--") or s.startswith("#"):
            continue
        if "verdict" not in s.lower() and "вердикт" not in s.lower():
            continue
        if re.search(r"(?<!<)\d{4}-\d{2}-\d{2}(?!>)", s):
            return True
    return False


def on_stop(project, text):
    missing = [label for label, pat in REQUIRED_SECTIONS
               if not re.search(pat, text, re.IGNORECASE | re.MULTILINE)]
    if "## Decisions" not in missing and not _has_real_decision(_section(text, "Decisions")):
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
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass  # older Python / non-reconfigurable stream — output may degrade, never crash
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
