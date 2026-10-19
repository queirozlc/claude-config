#!/usr/bin/env python3
"""Stop hook: refuse to end a turn with a stale ship ledger.

Blocks only when an open ledger exists for this repo AND the transcript shows a
cycle event (maestri ask, git commit, git push, gh pr) for that ledger's ticket
after the ledger's last write. An event belongs to the tickets its command
names; an event that names none belongs to the ledger whose Branch is checked
out. Silent everywhere else. Any failure exits 0: a hook must never wedge a
session.
"""
import json, os, re, subprocess, sys
from datetime import datetime, timezone

# A trigger counts only at a shell command boundary. Newline is deliberately not
# a boundary: a heredoc body that merely mentions `maestri ask` (editing the ship
# skill, say) is text, not a cycle event.
TRIGGER = re.compile(r"(?:^|&&|\|\||;|\|)\s*(?:maestri ask|git commit|git push|gh pr)\b")


def main():
    import ledger                           # ledger.py, beside this file: the one reader of ledgers
    ev = json.load(sys.stdin)
    if ev.get("stop_hook_active"):          # already blocked once, do not loop
        return
    cwd = ev.get("cwd") or os.getcwd()
    project = ledger.ship_project(cwd)
    if not project:
        return
    state = os.path.join(ledger.SHIP, "state", project)
    if not os.path.isdir(state):
        return

    ledgers = [(l["key"], l["path"], l["phase"], l["branch"]) for l in ledger.ledgers(state)[0] if l["open"]]
    keys = [key for key, *_ in ledgers]
    current = subprocess.run(["git", "-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
    stale = []
    for key, path, phase, branch in ledgers:
        def belongs(command):
            named = [k for k in keys if mentions(command, k)]
            return key in named if named else branch == current
        if worked_since(ev.get("transcript_path"), os.path.getmtime(path), belongs):
            stale.append((f"{key}.md", path, phase))

    if not stale:
        return
    lines = "\n".join(f"- {name} (Phase: {phase}) → {path}"
                      for name, path, phase in stale)
    print(json.dumps({"decision": "block", "reason": (
        "Ship ledger is stale. You ran a cycle event after its last write.\n"
        f"{lines}\n"
        "Append one `- HH:MM <what happened>` line to the ## Log, update the "
        "head only if a field changed, then stop. Do not rewrite the log.")}))


def mentions(command, key):
    """True if the command names the ticket key; EN-59 does not match inside EN-5913."""
    return re.search(rf"(?<![A-Za-z0-9]){re.escape(key)}(?![0-9])", command) is not None


def worked_since(transcript, mtime, belongs):
    """True if a Bash cycle-event tool call for this ledger ran after its last write."""
    if not transcript or not os.path.isfile(transcript):
        return False
    for line in open(transcript, errors="ignore"):
        try:
            ev = json.loads(line)
            when = datetime.fromisoformat(ev["timestamp"].replace("Z", "+00:00"))
        except Exception:
            continue
        if when.timestamp() <= mtime:
            continue
        content = ev.get("message", {}).get("content") or []
        for block in content if isinstance(content, list) else []:
            if not isinstance(block, dict) or block.get("name") != "Bash":
                continue
            command = block.get("input", {}).get("command", "")
            if TRIGGER.search(command) and belongs(command):
                return True
    return False


try:
    main()
except Exception:
    pass
